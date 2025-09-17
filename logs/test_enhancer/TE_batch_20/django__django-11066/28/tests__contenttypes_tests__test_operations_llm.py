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

from django.apps.registry import apps
from django.contrib.contenttypes import management as contenttypes_management
from django.contrib.contenttypes.models import ContentType
from django.db import connections, IntegrityError, router
from django.db import migrations
from django.test import TransactionTestCase, override_settings
from django.apps.registry import apps
from django.contrib.contenttypes import management as contenttypes_management
from django.contrib.contenttypes.models import ContentType
from django.db import connections, IntegrityError, router
from django.db import migrations
from django.test import TransactionTestCase, override_settings

class RenameContentTypeSaveTests(TransactionTestCase):
    databases = {'default', 'other'}
    available_apps = ['django.contrib.contenttypes']

    def test_clear_cache_called_on_success(self):
        ContentType.objects.using('other').create(app_label='test_app', model='old_model')
        rename_op = contenttypes_management.RenameContentType('test_app', 'old_model', 'new_model')
        original_clear = ContentType.objects.clear_cache
        called = {'flag': False}

        def mark_called():
            called['flag'] = True
            return original_clear()
        try:
            ContentType.objects.clear_cache = mark_called
            conn = connections['other']
            with conn.schema_editor() as schema_editor:
                rename_op._rename(apps, schema_editor, 'old_model', 'new_model')
            self.assertTrue(called['flag'], 'clear_cache() was not called on successful rename')
        finally:
            ContentType.objects.clear_cache = original_clear

from django.apps import apps
from django.db import connections, router, IntegrityError
from django.contrib.contenttypes.models import ContentType
from django.apps import apps
from django.conf import settings
from django.contrib.contenttypes.management import RenameContentType
from django.contrib.contenttypes.models import ContentType
from django.db import IntegrityError, connections, router
from django.test import TransactionTestCase, override_settings

class RenameContentTypeUsingDBTests(TransactionTestCase):
    databases = {'default', 'other'}
    available_apps = ['django.contrib.contenttypes']

    def setUp(self):
        ContentType.objects.using('default').filter(app_label__in=('rct_test', 'rct_conflict')).delete()
        ContentType.objects.using('other').filter(app_label__in=('rct_test', 'rct_conflict')).delete()

    def tearDown(self):
        ContentType.objects.using('default').filter(app_label__in=('rct_test', 'rct_conflict')).delete()
        ContentType.objects.using('other').filter(app_label__in=('rct_test', 'rct_conflict')).delete()

from unittest import mock
from django.db import connections

def test_rename_uses_schema_editor_db_despite_router(self):

    class BadRouter:

        def db_for_write(self, model, **hints):
            return 'default'

        def allow_migrate(self, db, app_label, model_name=None, **hints):
            return db == 'other'
    ContentType.objects.using('other').create(app_label='contenttypes_tests', model='foo')
    with mock.patch('django.conf.settings.DATABASE_ROUTERS', [BadRouter()]), override_settings(DATABASE_ROUTERS=[BadRouter()]):
        rename_op = contenttypes_management.RenameContentType('contenttypes_tests', 'foo', 'renamedfoo')
        conn = connections['other']
        with conn.schema_editor() as schema_editor:
            rename_op._rename(apps, schema_editor, 'foo', 'renamedfoo')
    self.assertFalse(ContentType.objects.using('other').filter(app_label='contenttypes_tests', model='foo').exists())
    self.assertTrue(ContentType.objects.using('other').filter(app_label='contenttypes_tests', model='renamedfoo').exists())
    self.assertFalse(ContentType.objects.using('default').filter(app_label='contenttypes_tests', model='renamedfoo').exists())

def test_rename_backward_uses_schema_editor_db(self):

    class BadRouter:

        def db_for_write(self, model, **hints):
            return 'default'

        def allow_migrate(self, db, app_label, model_name=None, **hints):
            return db == 'other'
    ContentType.objects.using('other').create(app_label='contenttypes_tests', model='renamedbar')
    with override_settings(DATABASE_ROUTERS=[BadRouter()]):
        rename_op = contenttypes_management.RenameContentType('contenttypes_tests', 'bar', 'renamedbar')
        conn = connections['other']
        with conn.schema_editor() as schema_editor:
            rename_op.rename_backward(apps, schema_editor)
    self.assertTrue(ContentType.objects.using('other').filter(app_label='contenttypes_tests', model='bar').exists())
    self.assertFalse(ContentType.objects.using('other').filter(app_label='contenttypes_tests', model='renamedbar').exists())
    self.assertFalse(ContentType.objects.using('default').filter(app_label='contenttypes_tests', model='bar').exists())

def test_missing_content_type_rename_does_nothing(self):

    class NeutralRouter:

        def db_for_write(self, model, **hints):
            return 'default'

        def allow_migrate(self, db, app_label, model_name=None, **hints):
            return True
    with override_settings(DATABASE_ROUTERS=[NeutralRouter()]):
        rename_op = contenttypes_management.RenameContentType('contenttypes_tests', 'nonexistent', 'stillnonexistent')
        conn = connections['other']
        with conn.schema_editor() as schema_editor:
            rename_op._rename(apps, schema_editor, 'nonexistent', 'stillnonexistent')
    self.assertFalse(ContentType.objects.using('other').filter(app_label='contenttypes_tests', model='stillnonexistent').exists())
    self.assertFalse(ContentType.objects.using('default').filter(app_label='contenttypes_tests', model='stillnonexistent').exists())

def test_rename_conflict_restores_old_value(self):
    ContentType.objects.using('other').create(app_label='contenttypes_tests', model='conflict_old')
    ContentType.objects.using('other').create(app_label='contenttypes_tests', model='conflict_new')

    class BadRouter:

        def db_for_write(self, model, **hints):
            return 'default'

        def allow_migrate(self, db, app_label, model_name=None, **hints):
            return db == 'other'
    with override_settings(DATABASE_ROUTERS=[BadRouter()]):
        rename_op = contenttypes_management.RenameContentType('contenttypes_tests', 'conflict_old', 'conflict_new')
        conn = connections['other']
        with conn.schema_editor() as schema_editor:
            rename_op._rename(apps, schema_editor, 'conflict_old', 'conflict_new')
    self.assertTrue(ContentType.objects.using('other').filter(app_label='contenttypes_tests', model='conflict_old').exists())
    self.assertTrue(ContentType.objects.using('other').filter(app_label='contenttypes_tests', model='conflict_new').exists())
    self.assertFalse(ContentType.objects.using('default').filter(app_label='contenttypes_tests', model='conflict_new').exists())

def test_clear_cache_called_on_successful_rename(self):
    ContentType.objects.using('other').create(app_label='contenttypes_tests', model='cachefoo')

    class BadRouter:

        def db_for_write(self, model, **hints):
            return 'default'

        def allow_migrate(self, db, app_label, model_name=None, **hints):
            return db == 'other'
    with override_settings(DATABASE_ROUTERS=[BadRouter()]):
        rename_op = contenttypes_management.RenameContentType('contenttypes_tests', 'cachefoo', 'cachenew')
        conn = connections['other']
        with conn.schema_editor() as schema_editor, mock.patch.object(ContentType.objects, 'clear_cache') as clear_cache_mock:
            rename_op._rename(apps, schema_editor, 'cachefoo', 'cachenew')
            clear_cache_mock.assert_called_once()
    self.assertTrue(ContentType.objects.using('other').filter(app_label='contenttypes_tests', model='cachenew').exists())

def test_clear_cache_not_called_on_conflict(self):
    ContentType.objects.using('other').create(app_label='contenttypes_tests', model='cacheconf_old')
    ContentType.objects.using('other').create(app_label='contenttypes_tests', model='cacheconf_new')

    class BadRouter:

        def db_for_write(self, model, **hints):
            return 'default'

        def allow_migrate(self, db, app_label, model_name=None, **hints):
            return db == 'other'
    with override_settings(DATABASE_ROUTERS=[BadRouter()]):
        rename_op = contenttypes_management.RenameContentType('contenttypes_tests', 'cacheconf_old', 'cacheconf_new')
        conn = connections['other']
        with conn.schema_editor() as schema_editor, mock.patch.object(ContentType.objects, 'clear_cache') as clear_cache_mock:
            rename_op._rename(apps, schema_editor, 'cacheconf_old', 'cacheconf_new')
            clear_cache_mock.assert_not_called()

def test_inject_rename_contenttypes_operations_inserts_after_rename_model(self):

    class FakeMigration:

        def __init__(self):
            self.app_label = 'someapp'
            self.name = '0002_auto'
            self.operations = [migrations.RenameModel('Foo', 'Bar'), migrations.CreateModel('Baz', fields=[])]
    migration = FakeMigration()
    plan = [(migration, False)]
    contenttypes_management.inject_rename_contenttypes_operations(plan=plan, apps=apps, using='default')
    ops = migration.operations
    found = False
    for i, op in enumerate(ops[:-1]):
        if isinstance(op, migrations.RenameModel):
            self.assertIsInstance(ops[i + 1], contenttypes_management.RenameContentType)
            found = True
            break
    self.assertTrue(found)

def test_inject_rename_contenttypes_operations_skips_when_contenttype_unavailable(self):

    class FakeAppsUnavailable:

        def get_model(self, app_label, model_name):
            raise LookupError

    class FakeMigration:

        def __init__(self):
            self.app_label = 'someapp'
            self.name = '0002_auto'
            self.operations = [migrations.RenameModel('Foo', 'Bar')]
    migration = FakeMigration()
    plan = [(migration, False)]
    contenttypes_management.inject_rename_contenttypes_operations(plan=plan, apps=FakeAppsUnavailable(), using='default')
    self.assertEqual(len(migration.operations), 1)
    self.assertIsInstance(migration.operations[0], migrations.RenameModel)

def test_get_contenttypes_and_models_respects_allow_migrate_model(self):
    ContentTypeModel = apps.get_model('contenttypes', 'ContentType')
    app_config = apps.get_app_config('contenttypes_tests')
    with mock.patch('django.contrib.contenttypes.management.router.allow_migrate_model', return_value=False):
        cts, models_map = contenttypes_management.get_contenttypes_and_models(app_config, 'default', ContentTypeModel)
        self.assertIsNone(cts)
        self.assertIsNone(models_map)

def test_rename_ignored_if_allow_migrate_model_false(self):
    ContentType.objects.using('other').create(app_label='contenttypes_tests', model='ignored_old')
    with mock.patch('django.contrib.contenttypes.management.router.allow_migrate_model', return_value=False):
        rename_op = contenttypes_management.RenameContentType('contenttypes_tests', 'ignored_old', 'ignored_new')
        conn = connections['other']
        with conn.schema_editor() as schema_editor:
            rename_op._rename(apps, schema_editor, 'ignored_old', 'ignored_new')
    self.assertTrue(ContentType.objects.using('other').filter(app_label='contenttypes_tests', model='ignored_old').exists())
    self.assertFalse(ContentType.objects.using('other').filter(app_label='contenttypes_tests', model='ignored_new').exists())

from django.db import connections, IntegrityError
from django.db import router
from django.apps.registry import apps
from django.conf import settings
from django.contrib.contenttypes import management as contenttypes_management
from django.contrib.contenttypes.models import ContentType
from django.db import IntegrityError, connections, router
from django.db import migrations
from django.test import TransactionTestCase, override_settings

@override_settings(MIGRATION_MODULES=dict(settings.MIGRATION_MODULES, contenttypes_tests='contenttypes_tests.operations_migrations'))
class RenameContentTypeRegressionTests(TransactionTestCase):
    databases = {'default', 'other'}
    available_apps = ['contenttypes_tests', 'django.contrib.contenttypes']

    def setUp(self):
        self._orig_allow = router.allow_migrate_model
        self.addCleanup(self._restore_router)

    def _restore_router(self):
        router.allow_migrate_model = self._orig_allow

from django.db import connections
from django.apps.registry import apps
from django.conf import settings
from django.contrib.contenttypes import management as contenttypes_management
from django.contrib.contenttypes.models import ContentType
from django.core.management import call_command
from django.db import migrations, models, IntegrityError
from django.test import override_settings

def _get_schema_editor(using):
    return connections[using].schema_editor()

def test_rename_updates_correct_database(self):
    ContentType.objects.using('other').create(app_label='contenttypes_tests', model='foo')
    rename_op = contenttypes_management.RenameContentType('contenttypes_tests', 'foo', 'renamedfoo')
    with connections['other'].schema_editor() as schema_editor:
        rename_op._rename(apps, schema_editor, 'foo', 'renamedfoo')
    self.assertTrue(ContentType.objects.using('other').filter(app_label='contenttypes_tests', model='renamedfoo').exists())
    self.assertFalse(ContentType.objects.using('default').filter(app_label='contenttypes_tests', model='renamedfoo').exists())

def test_rename_backward_updates_correct_database(self):
    ContentType.objects.using('other').create(app_label='contenttypes_tests', model='renamedfoo')
    rename_op = contenttypes_management.RenameContentType('contenttypes_tests', 'foo', 'renamedfoo')
    with connections['other'].schema_editor() as schema_editor:
        rename_op.rename_backward(apps, schema_editor)
    self.assertTrue(ContentType.objects.using('other').filter(app_label='contenttypes_tests', model='foo').exists())
    self.assertFalse(ContentType.objects.using('default').filter(app_label='contenttypes_tests', model='foo').exists())

def test_missing_content_type_rename_noop(self):
    ContentType.objects.using('other').filter(app_label='contenttypes_tests', model='nope').delete()
    rename_op = contenttypes_management.RenameContentType('contenttypes_tests', 'nope', 'stillnope')
    with connections['other'].schema_editor() as schema_editor:
        rename_op._rename(apps, schema_editor, 'nope', 'stillnope')
    self.assertFalse(ContentType.objects.using('other').filter(app_label='contenttypes_tests', model='stillnope').exists())
    self.assertFalse(ContentType.objects.using('default').filter(app_label='contenttypes_tests', model='stillnope').exists())

def test_rename_conflict_rolls_back_on_integrity_error(self):
    ContentType.objects.using('other').create(app_label='contenttypes_tests', model='foo')
    ContentType.objects.using('other').create(app_label='contenttypes_tests', model='renamedfoo')
    rename_op = contenttypes_management.RenameContentType('contenttypes_tests', 'foo', 'renamedfoo')
    with connections['other'].schema_editor() as schema_editor:
        rename_op._rename(apps, schema_editor, 'foo', 'renamedfoo')
    self.assertTrue(ContentType.objects.using('other').filter(app_label='contenttypes_tests', model='foo').exists())
    self.assertTrue(ContentType.objects.using('other').filter(app_label='contenttypes_tests', model='renamedfoo').exists())

def test_conflict_on_other_db_does_not_modify_default(self):
    ContentType.objects.using('other').create(app_label='contenttypes_tests', model='foo')
    ContentType.objects.using('default').create(app_label='contenttypes_tests', model='renamedfoo')
    rename_op = contenttypes_management.RenameContentType('contenttypes_tests', 'foo', 'renamedfoo')
    with connections['other'].schema_editor() as schema_editor:
        rename_op._rename(apps, schema_editor, 'foo', 'renamedfoo')
    self.assertTrue(ContentType.objects.using('other').filter(app_label='contenttypes_tests', model='foo').exists())
    self.assertTrue(ContentType.objects.using('default').filter(app_label='contenttypes_tests', model='renamedfoo').exists())

def test_rename_clears_cache_after_success(self):
    ContentType.objects.using('other').create(app_label='contenttypes_tests', model='foo')
    ct_old = ContentType.objects.using('other').get_by_natural_key('contenttypes_tests', 'foo')
    self.assertEqual(ct_old.model, 'foo')
    rename_op = contenttypes_management.RenameContentType('contenttypes_tests', 'foo', 'renamedfoo')
    with connections['other'].schema_editor() as schema_editor:
        rename_op._rename(apps, schema_editor, 'foo', 'renamedfoo')
    ct_new = ContentType.objects.using('other').get_by_natural_key('contenttypes_tests', 'renamedfoo')
    self.assertEqual(ct_new.model, 'renamedfoo')

@override_settings(DATABASE_ROUTERS=[DenyMigrateRouter()])
def test_rename_aborts_when_router_disallows_migration(self):
    ContentType.objects.using('other').create(app_label='contenttypes_tests', model='foo')
    rename_op = contenttypes_management.RenameContentType('contenttypes_tests', 'foo', 'renamedfoo')
    with connections['other'].schema_editor() as schema_editor:
        rename_op._rename(apps, schema_editor, 'foo', 'renamedfoo')
    self.assertTrue(ContentType.objects.using('other').filter(app_label='contenttypes_tests', model='foo').exists())
    self.assertFalse(ContentType.objects.using('other').filter(app_label='contenttypes_tests', model='renamedfoo').exists())

@override_settings(DATABASE_ROUTERS=[OtherDBRouter()])
def test_rename_respects_schema_editor_alias_when_saving(self):
    ContentType.objects.using('default').create(app_label='contenttypes_tests', model='foo')
    ContentType.objects.using('other').create(app_label='contenttypes_tests', model='foo')
    rename_op = contenttypes_management.RenameContentType('contenttypes_tests', 'foo', 'renamedfoo')
    with connections['other'].schema_editor() as schema_editor:
        rename_op._rename(apps, schema_editor, 'foo', 'renamedfoo')
    self.assertTrue(ContentType.objects.using('other').filter(app_label='contenttypes_tests', model='renamedfoo').exists())
    self.assertTrue(ContentType.objects.using('default').filter(app_label='contenttypes_tests', model='foo').exists())

def test_inject_rename_contenttypes_operations_inserts_operation(self):
    migration = migrations.Migration('0002_test', 'contenttypes_tests')
    migration.operations = [migrations.RenameModel('Foo', 'RenamedFoo')]
    plan = [(migration, False)]
    contenttypes_management.inject_rename_contenttypes_operations(plan=plan, apps=apps, using='default')
    self.assertEqual(len(migration.operations), 2)
    self.assertIsInstance(migration.operations[1], contenttypes_management.RenameContentType)
    inserted = migration.operations[1]
    self.assertEqual(inserted.app_label, migration.app_label)
    self.assertEqual(inserted.old_model, migration.operations[0].old_name_lower)
    self.assertEqual(inserted.new_model, migration.operations[0].new_name_lower)

@override_settings(DATABASE_ROUTERS=[DenyMigrateRouter()])
def test_get_contenttypes_and_models_respects_router(self):
    app_config = apps.get_app_config('contenttypes_tests')
    ContentTypeModel = ContentType
    content_types, app_models = contenttypes_management.get_contenttypes_and_models(app_config, 'other', ContentTypeModel)
    self.assertIsNone(content_types)
    self.assertIsNone(app_models)
for name, func in list(globals().items()):
    if name.startswith('test_'):
        setattr(ContentTypeOperationsTests, name, func)

from django.db import connections
from django.test import override_settings

def test__rename_uses_schema_editor_db_alias(self):
    """
    Ensure that RenameContentType._rename saves to the database identified by
    schema_editor.connection.alias (other DB), not the default DB.
    """
    ContentType.objects.using('other').create(app_label='contenttypes_tests', model='aliasmodel')
    self.assertFalse(ContentType.objects.filter(app_label='contenttypes_tests', model='aliasmodel').exists())
    rename_op = contenttypes_management.RenameContentType('contenttypes_tests', 'aliasmodel', 'aliasmodel_renamed')
    with connections['other'].schema_editor() as schema_editor:
        rename_op._rename(apps, schema_editor, 'aliasmodel', 'aliasmodel_renamed')
    self.assertFalse(ContentType.objects.using('other').filter(app_label='contenttypes_tests', model='aliasmodel').exists())
    self.assertTrue(ContentType.objects.using('other').filter(app_label='contenttypes_tests', model='aliasmodel_renamed').exists())
    self.assertFalse(ContentType.objects.filter(app_label='contenttypes_tests', model='aliasmodel_renamed').exists())

def test__rename_does_not_update_default_db(self):
    """
    If a content type exists in the 'other' DB, ensure renaming does not
    create or modify a ContentType in the default DB.
    """
    ContentType.objects.using('other').create(app_label='contenttypes_tests', model='othermodel')
    rename_op = contenttypes_management.RenameContentType('contenttypes_tests', 'othermodel', 'othermodel_new')
    with connections['other'].schema_editor() as schema_editor:
        rename_op._rename(apps, schema_editor, 'othermodel', 'othermodel_new')
    self.assertTrue(ContentType.objects.using('other').filter(app_label='contenttypes_tests', model='othermodel_new').exists())
    self.assertFalse(ContentType.objects.filter(app_label='contenttypes_tests', model='othermodel_new').exists())

def test__rename_conflict_on_other_db_resets_model(self):
    """
    If the target name already exists in the same database, the operation
    should catch IntegrityError and leave both rows unchanged.
    """
    ContentType.objects.using('other').create(app_label='contenttypes_tests', model='conflict_old')
    ContentType.objects.using('other').create(app_label='contenttypes_tests', model='conflict_new')
    rename_op = contenttypes_management.RenameContentType('contenttypes_tests', 'conflict_old', 'conflict_new')
    with connections['other'].schema_editor() as schema_editor:
        rename_op._rename(apps, schema_editor, 'conflict_old', 'conflict_new')
    self.assertTrue(ContentType.objects.using('other').filter(app_label='contenttypes_tests', model='conflict_old').exists())
    self.assertTrue(ContentType.objects.using('other').filter(app_label='contenttypes_tests', model='conflict_new').exists())

def test__rename_conflict_on_other_db_does_not_affect_default(self):
    """
    Ensure IntegrityError caused by conflict in 'other' DB does not
    mistakenly raise or alter data in the default DB.
    """
    ContentType.objects.using('other').create(app_label='contenttypes_tests', model='conflict2_old')
    ContentType.objects.using('other').create(app_label='contenttypes_tests', model='conflict2_new')
    self.assertFalse(ContentType.objects.filter(app_label='contenttypes_tests', model__in=('conflict2_old', 'conflict2_new')).exists())
    rename_op = contenttypes_management.RenameContentType('contenttypes_tests', 'conflict2_old', 'conflict2_new')
    with connections['other'].schema_editor() as schema_editor:
        rename_op._rename(apps, schema_editor, 'conflict2_old', 'conflict2_new')
    self.assertFalse(ContentType.objects.filter(app_label='contenttypes_tests', model__in=('conflict2_old', 'conflict2_new')).exists())

def test__rename_missing_content_type_is_noop(self):
    """
    If the old content type does not exist in the target DB, nothing should happen.
    """
    ContentType.objects.using('other').filter(app_label='contenttypes_tests', model='doesnotexist').delete()
    rename_op = contenttypes_management.RenameContentType('contenttypes_tests', 'doesnotexist', 'doesnotexist_new')
    with connections['other'].schema_editor() as schema_editor:
        rename_op._rename(apps, schema_editor, 'doesnotexist', 'doesnotexist_new')
    self.assertFalse(ContentType.objects.using('other').filter(app_label='contenttypes_tests', model='doesnotexist_new').exists())

def test__rename_backward_respects_db_alias(self):
    """
    Ensure rename_backward also uses the schema editor alias and undoes a prior rename.
    """
    ContentType.objects.using('other').create(app_label='contenttypes_tests', model='back_old')
    rename_op = contenttypes_management.RenameContentType('contenttypes_tests', 'back_old', 'back_new')
    with connections['other'].schema_editor() as schema_editor:
        rename_op.rename_forward(apps, schema_editor)
    self.assertTrue(ContentType.objects.using('other').filter(app_label='contenttypes_tests', model='back_new').exists())
    with connections['other'].schema_editor() as schema_editor:
        rename_op.rename_backward(apps, schema_editor)
    self.assertTrue(ContentType.objects.using('other').filter(app_label='contenttypes_tests', model='back_old').exists())
    self.assertFalse(ContentType.objects.using('other').filter(app_label='contenttypes_tests', model='back_new').exists())

@override_settings(DATABASE_ROUTERS=[type('NoMigrateRouter', (), {'allow_migrate': staticmethod(lambda db, app_label, model_name=None, **hints: False)})()])
def test__rename_skips_when_router_disallows_migration(self):
    """
    If router.allow_migrate_model returns False, the rename must be skipped
    and no changes made to either DB.
    """
    ContentType.objects.using('other').create(app_label='contenttypes_tests', model='skip_old')
    rename_op = contenttypes_management.RenameContentType('contenttypes_tests', 'skip_old', 'skip_new')
    with connections['other'].schema_editor() as schema_editor:
        rename_op._rename(apps, schema_editor, 'skip_old', 'skip_new')
    self.assertTrue(ContentType.objects.using('other').filter(app_label='contenttypes_tests', model='skip_old').exists())
    self.assertFalse(ContentType.objects.using('other').filter(app_label='contenttypes_tests', model='skip_new').exists())

def test__rename_succeeds_when_default_db_has_conflict(self):
    """
    If the default DB contains a ContentType with the target name but the
    target DB ('other') does not, the rename must proceed and affect only
    the 'other' DB. A save that doesn't pass using=db would incorrectly
    attempt to save to default and raise IntegrityError.
    """
    ContentType.objects.create(app_label='contenttypes_tests', model='global_conflict_new')
    ContentType.objects.using('other').create(app_label='contenttypes_tests', model='global_conflict_old')
    rename_op = contenttypes_management.RenameContentType('contenttypes_tests', 'global_conflict_old', 'global_conflict_new')
    with connections['other'].schema_editor() as schema_editor:
        rename_op._rename(apps, schema_editor, 'global_conflict_old', 'global_conflict_new')
    self.assertTrue(ContentType.objects.using('other').filter(app_label='contenttypes_tests', model='global_conflict_new').exists())
    self.assertTrue(ContentType.objects.filter(app_label='contenttypes_tests', model='global_conflict_new').exists())

def test__rename_transaction_atomic_uses_correct_db(self):
    """
    Ensure that the transaction.atomic(using=db) context manager is effective
    — i.e., the save runs in the same database context as the transaction.
    This is indirectly verified by ensuring the change appears only in that DB.
    """
    ContentType.objects.using('other').create(app_label='contenttypes_tests', model='txn_old')
    rename_op = contenttypes_management.RenameContentType('contenttypes_tests', 'txn_old', 'txn_new')
    with connections['other'].schema_editor() as schema_editor:
        rename_op._rename(apps, schema_editor, 'txn_old', 'txn_new')
    self.assertTrue(ContentType.objects.using('other').filter(app_label='contenttypes_tests', model='txn_new').exists())
    self.assertFalse(ContentType.objects.filter(app_label='contenttypes_tests', model='txn_new').exists())

from django.db import router, connections, IntegrityError
from django.apps.registry import apps
from django.conf import settings
from django.contrib.contenttypes import management as contenttypes_management
from django.contrib.contenttypes.models import ContentType
from django.db import connections, IntegrityError
from django.test import TransactionTestCase, override_settings
from django.db import router

class RenameContentTypeUsingDBTests(TransactionTestCase):
    databases = {'default', 'other'}
    available_apps = ['django.contrib.contenttypes']

    def _make_router_force_default(self):

        class ForcingDefaultRouter:

            def db_for_read(self, model, **hints):
                return 'default'

            def db_for_write(self, model, **hints):
                return 'default'

            def allow_migrate(self, db, app_label, model_name=None, **hints):
                return True
        return ForcingDefaultRouter()

from django.db import connections

def test_rename_direct_call_updates_target_db_only(self):
    ContentType.objects.using('other').create(app_label='ctops1', model='old1')
    self.assertFalse(ContentType.objects.using('default').filter(app_label='ctops1').exists())
    conn = __import__('django.db').db.connections['other']
    op = contenttypes_management.RenameContentType('ctops1', 'old1', 'new1')
    with conn.schema_editor() as schema_editor:
        op._rename(apps, schema_editor, 'old1', 'new1')
    self.assertTrue(ContentType.objects.using('other').filter(app_label='ctops1', model='new1').exists())
    self.assertFalse(ContentType.objects.using('default').filter(app_label='ctops1').exists())

@override_settings(DATABASE_ROUTERS=[TestRouter()])
def test_rename_with_write_router_updates_target_db_only(self):
    ContentType.objects.using('other').create(app_label='ctops2', model='old2')
    self.assertFalse(ContentType.objects.using('default').filter(app_label='ctops2').exists())
    conn = __import__('django.db').db.connections['other']
    op = contenttypes_management.RenameContentType('ctops2', 'old2', 'new2')
    with conn.schema_editor() as schema_editor:
        op._rename(apps, schema_editor, 'old2', 'new2')
    self.assertTrue(ContentType.objects.using('other').filter(app_label='ctops2', model='new2').exists())
    self.assertFalse(ContentType.objects.using('default').filter(app_label='ctops2').exists())

def test_rename_using_rename_forward_updates_target_db_only(self):
    ContentType.objects.using('other').create(app_label='ctops3', model='old3')
    conn = __import__('django.db').db.connections['other']
    op = contenttypes_management.RenameContentType('ctops3', 'old3', 'new3')
    with conn.schema_editor() as schema_editor:
        op.rename_forward(apps, schema_editor)
    self.assertTrue(ContentType.objects.using('other').filter(app_label='ctops3', model='new3').exists())
    self.assertFalse(ContentType.objects.using('default').filter(app_label='ctops3').exists())

@override_settings(DATABASE_ROUTERS=[TestRouter()])
def test_rename_using_rename_forward_with_router_updates_target_db_only(self):
    ContentType.objects.using('other').create(app_label='ctops4', model='old4')
    conn = __import__('django.db').db.connections['other']
    op = contenttypes_management.RenameContentType('ctops4', 'old4', 'new4')
    with conn.schema_editor() as schema_editor:
        op.rename_forward(apps, schema_editor)
    self.assertTrue(ContentType.objects.using('other').filter(app_label='ctops4', model='new4').exists())
    self.assertFalse(ContentType.objects.using('default').filter(app_label='ctops4').exists())

def test_rename_using_rename_backward_updates_target_db_only(self):
    ContentType.objects.using('other').create(app_label='ctops5', model='new5')
    conn = __import__('django.db').db.connections['other']
    op = contenttypes_management.RenameContentType('ctops5', 'old5', 'new5')
    with conn.schema_editor() as schema_editor:
        op.rename_backward(apps, schema_editor)
    self.assertTrue(ContentType.objects.using('other').filter(app_label='ctops5', model='old5').exists())
    self.assertFalse(ContentType.objects.using('default').filter(app_label='ctops5').exists())

@override_settings(DATABASE_ROUTERS=[TestRouter()])
def test_rename_using_rename_backward_with_router_updates_target_db_only(self):
    ContentType.objects.using('other').create(app_label='ctops6', model='new6')
    conn = __import__('django.db').db.connections['other']
    op = contenttypes_management.RenameContentType('ctops6', 'old6', 'new6')
    with conn.schema_editor() as schema_editor:
        op.rename_backward(apps, schema_editor)
    self.assertTrue(ContentType.objects.using('other').filter(app_label='ctops6', model='old6').exists())
    self.assertFalse(ContentType.objects.using('default').filter(app_label='ctops6').exists())

@override_settings(DATABASE_ROUTERS=[TestRouter()])
def test_missing_content_type_does_nothing_with_router(self):
    self.assertFalse(ContentType.objects.using('other').filter(app_label='ctops7').exists())
    self.assertFalse(ContentType.objects.using('default').filter(app_label='ctops7').exists())
    conn = __import__('django.db').db.connections['other']
    op = contenttypes_management.RenameContentType('ctops7', 'doesnotexist', 'new7')
    with conn.schema_editor() as schema_editor:
        op._rename(apps, schema_editor, 'doesnotexist', 'new7')
    self.assertFalse(ContentType.objects.using('other').filter(app_label='ctops7').exists())
    self.assertFalse(ContentType.objects.using('default').filter(app_label='ctops7').exists())

def test_missing_content_type_does_nothing_without_router(self):
    self.assertFalse(ContentType.objects.using('other').filter(app_label='ctops8').exists())
    self.assertFalse(ContentType.objects.using('default').filter(app_label='ctops8').exists())
    conn = __import__('django.db').db.connections['other']
    op = contenttypes_management.RenameContentType('ctops8', 'doesnotexist', 'new8')
    with conn.schema_editor() as schema_editor:
        op._rename(apps, schema_editor, 'doesnotexist', 'new8')
    self.assertFalse(ContentType.objects.using('other').filter(app_label='ctops8').exists())
    self.assertFalse(ContentType.objects.using('default').filter(app_label='ctops8').exists())

def test_rename_multiple_models_updates_only_target_db(self):
    ContentType.objects.using('other').create(app_label='ctops9', model='old9a')
    ContentType.objects.using('other').create(app_label='ctops9', model='old9b')
    conn = __import__('django.db').db.connections['other']
    op1 = contenttypes_management.RenameContentType('ctops9', 'old9a', 'new9a')
    op2 = contenttypes_management.RenameContentType('ctops9', 'old9b', 'new9b')
    with conn.schema_editor() as schema_editor:
        op1._rename(apps, schema_editor, 'old9a', 'new9a')
        op2._rename(apps, schema_editor, 'old9b', 'new9b')
    self.assertTrue(ContentType.objects.using('other').filter(app_label='ctops9', model='new9a').exists())
    self.assertTrue(ContentType.objects.using('other').filter(app_label='ctops9', model='new9b').exists())
    self.assertFalse(ContentType.objects.using('default').filter(app_label='ctops9').exists())

def test_rename_does_not_create_in_default_when_default_has_unrelated_entry(self):
    ContentType.objects.using('default').create(app_label='unrelated_app', model='foo')
    ContentType.objects.using('other').create(app_label='ctops10', model='old10')
    conn = __import__('django.db').db.connections['other']
    op = contenttypes_management.RenameContentType('ctops10', 'old10', 'new10')
    with conn.schema_editor() as schema_editor:
        op._rename(apps, schema_editor, 'old10', 'new10')
    self.assertTrue(ContentType.objects.using('other').filter(app_label='ctops10', model='new10').exists())
    self.assertTrue(ContentType.objects.using('default').filter(app_label='unrelated_app', model='foo').exists())
    self.assertFalse(ContentType.objects.using('default').filter(app_label='ctops10').exists())

from unittest.mock import patch
from django.apps.registry import apps
from django.contrib.contenttypes import management as contenttypes_management
from django.contrib.contenttypes.models import ContentType
from django.db import connections
from django.db.utils import IntegrityError
from django.test import TransactionTestCase

class RenameContentTypeDBTests(TransactionTestCase):
    databases = {'default', 'other'}
    available_apps = ['contenttypes_tests', 'django.contrib.contenttypes']

    def test_clear_cache_called_on_success(self):
        ContentType.objects.using('other').create(app_label='contenttypes_tests', model='foo')
        op = contenttypes_management.RenameContentType('contenttypes_tests', 'foo', 'renamedfoo')
        with patch.object(ContentType.objects, 'clear_cache') as mock_clear:
            with connections['other'].schema_editor() as schema_editor:
                op._rename(apps, schema_editor, 'foo', 'renamedfoo')
            mock_clear.assert_called_once()