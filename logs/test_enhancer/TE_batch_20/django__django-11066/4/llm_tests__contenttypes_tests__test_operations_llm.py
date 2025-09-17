from django.apps.registry import apps
from django.conf import settings
from django.contrib.contenttypes import management as contenttypes_management
from django.contrib.contenttypes.models import ContentType
from django.db import connections, transaction
from django.db.utils import IntegrityError
from django.test import override_settings
from django.apps.registry import apps
from django.conf import settings
from django.contrib.contenttypes import management as contenttypes_management
from django.contrib.contenttypes.models import ContentType
from django.db import connections, transaction
from django.db.utils import IntegrityError
from django.test import override_settings

def test_save_called_with_using_on_direct_rename_default_db():
    ContentType.objects.using('default').create(app_label='ct_test_app', model='oldmodel')
    rename = contenttypes_management.RenameContentType('ct_test_app', 'oldmodel', 'newmodel')
    called = {}
    original_save = ContentType.save

    def spy_save(self, *args, **kwargs):
        called['kwargs'] = kwargs.copy()
        return original_save(self, *args, **kwargs)
    ContentType.save = spy_save
    try:
        connection = connections['default']
        with connection.schema_editor() as schema_editor:
            rename._rename(apps, schema_editor, 'oldmodel', 'newmodel')
        assert 'kwargs' in called, 'ContentType.save was not called'
        assert called['kwargs'].get('using') == 'default'
        assert not ContentType.objects.using('default').filter(app_label='ct_test_app', model='oldmodel').exists()
        assert ContentType.objects.using('default').filter(app_label='ct_test_app', model='newmodel').exists()
    finally:
        ContentType.save = original_save

def test_save_called_with_using_on_direct_rename_other_db():
    ContentType.objects.using('other').create(app_label='ct_test_app_other', model='oldmodel')
    rename = contenttypes_management.RenameContentType('ct_test_app_other', 'oldmodel', 'newmodel')
    called = {}
    original_save = ContentType.save

    def spy_save(self, *args, **kwargs):
        called['kwargs'] = kwargs.copy()
        return original_save(self, *args, **kwargs)
    ContentType.save = spy_save
    try:
        connection = connections['other']
        with connection.schema_editor() as schema_editor:
            rename._rename(apps, schema_editor, 'oldmodel', 'newmodel')
        assert 'kwargs' in called, 'ContentType.save was not called'
        assert called['kwargs'].get('using') == 'other'
        assert not ContentType.objects.using('other').filter(app_label='ct_test_app_other', model='oldmodel').exists()
        assert ContentType.objects.using('other').filter(app_label='ct_test_app_other', model='newmodel').exists()
        assert not ContentType.objects.using('default').filter(app_label='ct_test_app_other').exists()
    finally:
        ContentType.save = original_save

def test_rename_does_not_affect_other_db_when_running_on_one_db():
    ContentType.objects.using('default').create(app_label='ct_both', model='same')
    ContentType.objects.using('other').create(app_label='ct_both', model='same')
    rename = contenttypes_management.RenameContentType('ct_both', 'same', 'changed')
    connection = connections['other']
    with connection.schema_editor() as schema_editor:
        rename._rename(apps, schema_editor, 'same', 'changed')
    assert ContentType.objects.using('other').filter(app_label='ct_both', model='changed').exists()
    assert ContentType.objects.using('default').filter(app_label='ct_both', model='same').exists()

def test_rename_roundtrip_forward_backward_preserves_db_alias():
    ContentType.objects.using('other').create(app_label='ct_round', model='a')
    rename = contenttypes_management.RenameContentType('ct_round', 'a', 'b')
    connection = connections['other']
    with connection.schema_editor() as schema_editor:
        rename.rename_forward(apps, schema_editor)
    assert ContentType.objects.using('other').filter(app_label='ct_round', model='b').exists()
    with connection.schema_editor() as schema_editor:
        rename.rename_backward(apps, schema_editor)
    assert ContentType.objects.using('other').filter(app_label='ct_round', model='a').exists()

def test_missing_content_type_no_error_and_no_save_called():
    ContentType.objects.using('default').filter(app_label='ct_missing').delete()
    rename = contenttypes_management.RenameContentType('ct_missing', 'doesnotexist', 'newname')
    called = {'called': False}
    original_save = ContentType.save

    def spy_save(self, *args, **kwargs):
        called['called'] = True
        return original_save(self, *args, **kwargs)
    ContentType.save = spy_save
    try:
        connection = connections['default']
        with connection.schema_editor() as schema_editor:
            rename._rename(apps, schema_editor, 'doesnotexist', 'newname')
        assert not called['called'], 'save() should not be called for missing content types'
    finally:
        ContentType.save = original_save

def test_integrity_error_restores_old_model_and_does_not_clear_cache():
    ContentType.objects.using('other').create(app_label='ct_conflict', model='orig')
    rename = contenttypes_management.RenameContentType('ct_conflict', 'orig', 'newname')
    clear_called = {'count': 0}
    original_clear = ContentType.objects.clear_cache

    def spy_clear():
        clear_called['count'] += 1
    ContentType.objects.clear_cache = spy_clear
    original_save = ContentType.save

    def raising_save(self, *args, **kwargs):
        if kwargs.get('using') == 'other':
            raise IntegrityError('simulate conflict')
        return original_save(self, *args, **kwargs)
    ContentType.save = raising_save
    try:
        connection = connections['other']
        with connection.schema_editor() as schema_editor:
            rename._rename(apps, schema_editor, 'orig', 'newname')
        assert ContentType.objects.using('other').filter(app_label='ct_conflict', model='orig').exists()
        assert not ContentType.objects.using('other').filter(app_label='ct_conflict', model='newname').exists()
        assert clear_called['count'] == 0
    finally:
        ContentType.save = original_save
        ContentType.objects.clear_cache = original_clear

def test_clear_cache_called_on_successful_rename():
    ContentType.objects.using('default').create(app_label='ct_cache', model='x')
    rename = contenttypes_management.RenameContentType('ct_cache', 'x', 'y')
    called = {'count': 0}
    original_clear = ContentType.objects.clear_cache

    def spy_clear():
        called['count'] += 1
    ContentType.objects.clear_cache = spy_clear
    try:
        connection = connections['default']
        with connection.schema_editor() as schema_editor:
            rename._rename(apps, schema_editor, 'x', 'y')
        assert called['count'] == 1, 'clear_cache should be called once on successful rename'
    finally:
        ContentType.objects.clear_cache = original_clear

def test_save_using_passed_in_rename_forward():
    ContentType.objects.using('other').create(app_label='ct_forward', model='m1')
    rename = contenttypes_management.RenameContentType('ct_forward', 'm1', 'm2')
    captured = {}
    original_save = ContentType.save

    def spy_save(self, *args, **kwargs):
        captured['using'] = kwargs.get('using')
        return original_save(self, *args, **kwargs)
    ContentType.save = spy_save
    try:
        connection = connections['other']
        with connection.schema_editor() as schema_editor:
            rename.rename_forward(apps, schema_editor)
        assert captured.get('using') == 'other'
    finally:
        ContentType.save = original_save

def test_save_using_passed_in_rename_backward():
    ContentType.objects.using('default').create(app_label='ct_back', model='origback')
    rename = contenttypes_management.RenameContentType('ct_back', 'origback', 'tmpname')
    captured = {}
    original_save = ContentType.save

    def spy_save(self, *args, **kwargs):
        captured['using'] = kwargs.get('using')
        return original_save(self, *args, **kwargs)
    ContentType.save = spy_save
    try:
        connection = connections['default']
        with connection.schema_editor() as schema_editor:
            rename.rename_backward(apps, schema_editor)
        assert captured.get('using') == 'default'
    finally:
        ContentType.save = original_save