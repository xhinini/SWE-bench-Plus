import tempfile
from pathlib import Path
from django.core.files.storage import FileSystemStorage, default_storage
from django.db.models.fields.files import FileField

def test_deconstruct_omits_default_storage():
    f = FileField(storage=default_storage, upload_to='tests')
    name, path, args, kwargs = f.deconstruct()
    assert 'storage' not in kwargs

def test_deconstruct_includes_custom_storage_instance():
    temp_dir = tempfile.mkdtemp()
    fs = FileSystemStorage(location=temp_dir)
    f = FileField(storage=fs, upload_to='tests')
    name, path, args, kwargs = f.deconstruct()
    assert 'storage' in kwargs
    assert kwargs['storage'] is fs

def test_deconstruct_includes_callable_storage():
    temp_dir = tempfile.mkdtemp()
    fs = FileSystemStorage(location=temp_dir)

    def my_callable():
        return fs
    f = FileField(storage=my_callable, upload_to='tests')
    name, path, args, kwargs = f.deconstruct()
    assert 'storage' in kwargs
    assert kwargs['storage'] is my_callable

def test_deconstruct_includes_class_callable():

    class MyStorage(FileSystemStorage):

        def __call__(self):
            return self
    f = FileField(storage=MyStorage, upload_to='tests')
    name, path, args, kwargs = f.deconstruct()
    assert 'storage' in kwargs
    assert kwargs['storage'] is MyStorage

def test_deconstruct_includes_callable_that_returns_default_storage():

    def callable_default():
        return default_storage
    f = FileField(storage=callable_default, upload_to='tests')
    name, path, args, kwargs = f.deconstruct()
    assert 'storage' in kwargs
    assert kwargs['storage'] is callable_default

def test_deconstruct_omits_storage_when__storage_callable_set_to_default_storage_on_default_init():
    f = FileField(storage=default_storage, upload_to='tests')
    f._storage_callable = default_storage
    name, path, args, kwargs = f.deconstruct()
    assert 'storage' not in kwargs

def test_deconstruct_omits_storage_when__storage_callable_set_to_default_storage_even_if_instance_was_custom():
    temp_dir = tempfile.mkdtemp()
    fs = FileSystemStorage(location=temp_dir)
    f = FileField(storage=fs, upload_to='tests')
    f._storage_callable = default_storage
    name, path, args, kwargs = f.deconstruct()
    assert 'storage' not in kwargs

def test_deconstruct_omits_storage_when__storage_callable_overwrites_callable_and_set_to_default_storage():

    def callable_default():
        return default_storage
    f = FileField(storage=callable_default, upload_to='tests')
    f._storage_callable = default_storage
    name, path, args, kwargs = f.deconstruct()
    assert 'storage' not in kwargs

def test_deconstruct_removes_default_max_length():
    f = FileField(upload_to='tests')
    name, path, args, kwargs = f.deconstruct()
    assert 'max_length' not in kwargs

def test_deconstruct_preserves_upload_to_values():
    f1 = FileField(upload_to=Path('bar'))
    name, path, args, kwargs = f1.deconstruct()
    assert kwargs['upload_to'] == Path('bar')

    def upload_callable(instance, filename):
        return 'x'
    f2 = FileField(upload_to=upload_callable)
    name, path, args, kwargs = f2.deconstruct()
    assert kwargs['upload_to'] is upload_callable

import tempfile
from django.db.models.fields.files import FileField
from django.core.files.storage import FileSystemStorage, default_storage

def test_deconstruct_omits_storage_for_default_storage_instance():
    field = FileField(upload_to='tests', storage=default_storage)
    name, path, args, kwargs = field.deconstruct()
    assert 'storage' not in kwargs

def test_deconstruct_includes_storage_for_custom_storage_instance():
    tmpdir = tempfile.mkdtemp()
    custom = FileSystemStorage(location=tmpdir)
    field = FileField(upload_to='tests', storage=custom)
    name, path, args, kwargs = field.deconstruct()
    assert 'storage' in kwargs
    assert kwargs['storage'] is custom

def test_deconstruct_includes_callable_storage_object_not_result():
    tmpdir = tempfile.mkdtemp()

    def make_storage():
        return FileSystemStorage(location=tmpdir)
    field = FileField(upload_to='tests', storage=make_storage)
    name, path, args, kwargs = field.deconstruct()
    assert 'storage' in kwargs
    assert kwargs['storage'] is make_storage

def test_deconstruct_includes_callable_that_returns_default_storage():

    def make_default():
        return default_storage
    field = FileField(upload_to='tests', storage=make_default)
    name, path, args, kwargs = field.deconstruct()
    assert 'storage' in kwargs
    assert kwargs['storage'] is make_default

def test_deconstruct_includes_callable_class_object():

    class MyCallableStorage(FileSystemStorage):

        def __call__(self):
            return self
    field = FileField(upload_to='tests', storage=MyCallableStorage)
    name, path, args, kwargs = field.deconstruct()
    assert 'storage' in kwargs
    assert kwargs['storage'] is MyCallableStorage

def test_deconstruct_includes_function_that_creates_storage_each_time():
    tmpdir = tempfile.mkdtemp()

    def factory():
        return FileSystemStorage(location=tmpdir)
    field = FileField(upload_to='tests', storage=factory)
    name, path, args, kwargs = field.deconstruct()
    assert 'storage' in kwargs
    assert kwargs['storage'] is factory

def test_deconstruct_drops_default_max_length():
    field = FileField(upload_to='tests', storage=default_storage)
    name, path, args, kwargs = field.deconstruct()
    assert 'max_length' not in kwargs

def test_deconstruct_preserves_non_default_max_length():
    tmpdir = tempfile.mkdtemp()
    custom = FileSystemStorage(location=tmpdir)
    field = FileField(upload_to='tests', storage=custom, max_length=300)
    name, path, args, kwargs = field.deconstruct()
    assert 'max_length' in kwargs
    assert kwargs['max_length'] == 300

def test_deconstruct_callable_returning_default_storage_is_callable_in_kwargs():

    def get_default():
        return default_storage
    field = FileField(upload_to='tests', storage=get_default)
    name, path, args, kwargs = field.deconstruct()
    assert 'storage' in kwargs
    assert kwargs['storage'] is get_default
    assert kwargs['storage'] is not default_storage

def test_deconstruct_includes_callable_when_storage_instance_is_default_storage():

    def caller_default():
        return default_storage
    field = FileField(upload_to='tests', storage=caller_default)
    assert field.storage is default_storage
    name, path, args, kwargs = field.deconstruct()
    assert 'storage' in kwargs
    assert kwargs['storage'] is caller_default

from tests.file_storage.models import Storage, temp_storage, callable_storage, callable_default_storage, CallableStorage
import inspect
import pytest
from django.core.files.storage import default_storage
from django.db.models.fields.files import FileField
from tests.file_storage import models as fs_models

def _deconstruct_field(field):
    name, path, args, kwargs = field.deconstruct()
    return kwargs

def test_deconstruct_includes_callable_storage_function():
    field = fs_models.Storage._meta.get_field('storage_callable')
    kwargs = _deconstruct_field(field)
    assert 'storage' in kwargs
    assert kwargs['storage'] is fs_models.callable_storage

def test_deconstruct_includes_callable_storage_class():
    field = fs_models.Storage._meta.get_field('storage_callable_class')
    kwargs = _deconstruct_field(field)
    assert 'storage' in kwargs
    assert kwargs['storage'] is fs_models.CallableStorage

def test_deconstruct_includes_callable_that_returns_default_storage():
    field = fs_models.Storage._meta.get_field('storage_callable_default')
    kwargs = _deconstruct_field(field)
    assert 'storage' in kwargs
    assert kwargs['storage'] is fs_models.callable_default_storage

def test_deconstruct_includes_storage_instance_for_explicit_instance():
    field = fs_models.Storage._meta.get_field('normal')
    kwargs = _deconstruct_field(field)
    assert 'storage' in kwargs
    assert kwargs['storage'] is fs_models.temp_storage

def test_deconstruct_excludes_default_storage_instance():
    ff = FileField(storage=default_storage)
    kwargs = _deconstruct_field(ff)
    assert 'storage' not in kwargs

def test_deconstruct_preserves_identity_of_callable_storage():
    field = fs_models.Storage._meta.get_field('storage_callable')
    kwargs = _deconstruct_field(field)
    storage_obj = kwargs['storage']
    assert inspect.isfunction(storage_obj) or inspect.isbuiltin(storage_obj) or inspect.isclass(storage_obj)
    assert storage_obj is fs_models.callable_storage

def test_deconstruct_preserves_identity_of_callable_returning_default():
    field = fs_models.Storage._meta.get_field('storage_callable_default')
    kwargs = _deconstruct_field(field)
    storage_obj = kwargs['storage']
    assert callable(storage_obj)
    assert storage_obj is fs_models.callable_default_storage

def test_deconstruct_for_field_with_default_value_and_custom_storage():
    field = fs_models.Storage._meta.get_field('default')
    kwargs = _deconstruct_field(field)
    assert 'storage' in kwargs
    assert kwargs['storage'] is fs_models.temp_storage

def test_deconstruct_for_empty_field_with_custom_storage():
    field = fs_models.Storage._meta.get_field('empty')
    kwargs = _deconstruct_field(field)
    assert 'storage' in kwargs
    assert kwargs['storage'] is fs_models.temp_storage

def test_deconstruct_for_storage_callable_class_instance_behaves_like_callable():
    field = fs_models.Storage._meta.get_field('storage_callable_class')
    kwargs = _deconstruct_field(field)
    assert 'storage' in kwargs
    assert kwargs['storage'] is fs_models.CallableStorage

import inspect
from pathlib import Path
import pytest
from django.core.files.storage import default_storage
from django.db.models.fields.files import FileField
from tests.file_storage.models import Storage, temp_storage, callable_storage, callable_default_storage, CallableStorage

def test_deconstruct_includes_storage_when_callable_returns_default_storage():
    """
    When storage was given as a callable that returns default_storage,
    deconstruct() should include the original callable in kwargs['storage'].
    """
    field = Storage._meta.get_field('storage_callable_default')
    name, path, args, kwargs = field.deconstruct()
    assert 'storage' in kwargs
    assert kwargs['storage'] is callable_default_storage

def test_deconstruct_includes_storage_when_callable_returns_non_default_storage():
    """
    A callable storage that returns a non-default storage should be preserved
    (the callable itself should be present in kwargs['storage']).
    """
    field = Storage._meta.get_field('storage_callable')
    name, path, args, kwargs = field.deconstruct()
    assert 'storage' in kwargs
    assert kwargs['storage'] is callable_storage

def test_deconstruct_includes_storage_when_storage_passed_as_instance():
    """
    When storage is passed as a non-default Storage instance, deconstruct()
    should include that instance in kwargs['storage'].
    """
    field = Storage._meta.get_field('normal')
    name, path, args, kwargs = field.deconstruct()
    assert 'storage' in kwargs
    assert kwargs['storage'] is temp_storage

def test_deconstruct_excludes_storage_when_using_default_storage_instance():
    """
    If the field is using the module-level default_storage instance and no
    callable was provided, deconstruct() should NOT include a 'storage' kwarg.
    """
    f = FileField()
    name, path, args, kwargs = f.deconstruct()
    assert 'storage' not in kwargs

def test_deconstruct_preserves_callable_class_as_storage():
    """
    If the storage argument was a callable class (not an instance), the class
    itself should be preserved in deconstruct() kwargs.
    """
    field = Storage._meta.get_field('storage_callable_class')
    name, path, args, kwargs = field.deconstruct()
    assert 'storage' in kwargs
    assert kwargs['storage'] is CallableStorage

def test_deconstruct_removes_default_max_length():
    """
    The default max_length (100) should not be present in deconstruct kwargs.
    """
    field = Storage._meta.get_field('normal')
    name, path, args, kwargs = field.deconstruct()
    assert 'max_length' not in kwargs

def test_deconstruct_preserves_pathlib_upload_to():
    """
    If upload_to was provided as a pathlib.Path, it should be preserved
    exactly in deconstruct() kwargs.
    """
    field = Storage._meta.get_field('pathlib_direct')
    name, path, args, kwargs = field.deconstruct()
    assert 'upload_to' in kwargs
    assert kwargs['upload_to'] == Path('bar')

def test_deconstruct_preserves_callable_identity_for_storage_callable():
    """
    Ensure the exact callable object passed as storage is returned by deconstruct.
    """
    field = Storage._meta.get_field('storage_callable')
    name, path, args, kwargs = field.deconstruct()
    assert kwargs['storage'] is callable_storage
    assert callable(kwargs['storage'])

def test_deconstruct_includes_callable_even_if_it_returns_default_storage_explicit_check():
    """
    Double-check with the explicit callable defined in tests that returns
    default_storage that it's preserved in deconstruct kwargs.
    """
    field = Storage._meta.get_field('storage_callable_default')
    name, path, args, kwargs = field.deconstruct()
    assert 'storage' in kwargs
    assert kwargs['storage'] is callable_default_storage
    assert kwargs['storage']() is default_storage

def test_deconstruct_includes_storage_callable_class_when_instance_is_callable():
    """
    For callable classes/instances that are callable and return themselves,
    deconstruct should still preserve the original callable (class).
    This verifies that storage_callable_class was preserved as the class object.
    """
    field = Storage._meta.get_field('storage_callable_class')
    name, path, args, kwargs = field.deconstruct()
    assert 'storage' in kwargs
    assert kwargs['storage'] is CallableStorage

import types
import pytest
from django.core.files.storage import default_storage
from django.db.models.fields.files import FileField
from tests.file_storage.models import temp_storage, callable_storage, callable_default_storage, CallableStorage, callable_storage as callable_returns_temp_storage

def test_deconstruct_with_default_storage_no_callable():
    field = FileField(storage=default_storage)
    name, path, args, kwargs = field.deconstruct()
    assert 'storage' not in kwargs

def test_deconstruct_with_non_default_storage_included():
    field = FileField(storage=temp_storage)
    name, path, args, kwargs = field.deconstruct()
    assert 'storage' in kwargs
    assert kwargs['storage'] is temp_storage

def test_deconstruct_with_callable_returning_non_default_included():
    field = FileField(storage=callable_storage)
    name, path, args, kwargs = field.deconstruct()
    assert 'storage' in kwargs
    assert kwargs['storage'] is callable_storage

def test_deconstruct_with_callable_returning_default_included():
    field = FileField(storage=callable_default_storage)
    name, path, args, kwargs = field.deconstruct()
    assert 'storage' in kwargs
    assert kwargs['storage'] is callable_default_storage

def test_deconstruct_with_callable_class_included():
    field = FileField(storage=CallableStorage)
    name, path, args, kwargs = field.deconstruct()
    assert 'storage' in kwargs
    assert kwargs['storage'] is CallableStorage

def test_deconstruct_do_not_include_storage_when__storage_callable_is_default_and_storage_is_default():
    field = FileField(storage=default_storage)
    field._storage_callable = default_storage
    name, path, args, kwargs = field.deconstruct()
    assert 'storage' not in kwargs

def test_deconstruct_do_not_include_storage_when__storage_callable_is_default_and_storage_is_non_default():
    field = FileField(storage=temp_storage)
    field._storage_callable = default_storage
    name, path, args, kwargs = field.deconstruct()
    assert 'storage' not in kwargs

def test_deconstruct_do_not_include_storage_when__storage_callable_is_default_and_initial_was_callable():
    field = FileField(storage=callable_returns_temp_storage)
    field._storage_callable = default_storage
    name, path, args, kwargs = field.deconstruct()
    assert 'storage' not in kwargs

def test_deconstruct_do_not_include_storage_when__storage_callable_is_default_and_initial_was_callable_default():
    field = FileField(storage=callable_default_storage)
    field._storage_callable = default_storage
    name, path, args, kwargs = field.deconstruct()
    assert 'storage' not in kwargs

def test_deconstruct_do_not_include_storage_when__storage_callable_is_default_and_initial_was_callable_class():
    field = FileField(storage=CallableStorage)
    field._storage_callable = default_storage
    name, path, args, kwargs = field.deconstruct()
    assert 'storage' not in kwargs

import types
from django.core.files.storage import default_storage
from django.db.models.fields.files import FileField
from tests.file_storage import models as storage_models

def test_deconstruct_includes_temp_storage_instance():
    field = storage_models.Storage._meta.get_field('normal')
    name, path, args, kwargs = field.deconstruct()
    assert 'storage' in kwargs
    assert kwargs['storage'] is storage_models.temp_storage

def test_deconstruct_includes_custom_valid_name_storage_instance():
    field = storage_models.Storage._meta.get_field('custom_valid_name')
    name, path, args, kwargs = field.deconstruct()
    assert 'storage' in kwargs
    assert isinstance(kwargs['storage'], storage_models.CustomValidNameStorage)
    assert getattr(kwargs['storage'], 'location', None) == storage_models.temp_storage_location

def test_deconstruct_includes_callable_storage_function():
    field = storage_models.Storage._meta.get_field('storage_callable')
    name, path, args, kwargs = field.deconstruct()
    assert 'storage' in kwargs
    assert kwargs['storage'] is storage_models.callable_storage
    assert isinstance(kwargs['storage'], types.FunctionType)

def test_deconstruct_includes_callable_storage_class():
    field = storage_models.Storage._meta.get_field('storage_callable_class')
    name, path, args, kwargs = field.deconstruct()
    assert 'storage' in kwargs
    assert kwargs['storage'] is storage_models.CallableStorage

def test_deconstruct_includes_callable_returning_default_storage():
    field = storage_models.Storage._meta.get_field('storage_callable_default')
    name, path, args, kwargs = field.deconstruct()
    assert 'storage' in kwargs
    assert kwargs['storage'] is storage_models.callable_default_storage
    assert callable(kwargs['storage'])

def test_deconstruct_omits_storage_for_direct_default_storage_instance():
    f = FileField(storage=default_storage)
    name, path, args, kwargs = f.deconstruct()
    assert 'storage' not in kwargs

def test_deconstruct_includes_callable_returning_default_storage_when_field_instantiated_directly():
    f = FileField(storage=storage_models.callable_default_storage)
    name, path, args, kwargs = f.deconstruct()
    assert 'storage' in kwargs
    assert kwargs['storage'] is storage_models.callable_default_storage

def test_deconstruct_includes_callable_class_when_field_instantiated_directly():
    f = FileField(storage=storage_models.CallableStorage)
    name, path, args, kwargs = f.deconstruct()
    assert 'storage' in kwargs
    assert kwargs['storage'] is storage_models.CallableStorage

def test_deconstruct_preserves_storage_identity_for_callable_from_model_field():
    field = storage_models.Storage._meta.get_field('storage_callable')
    _, _, _, kwargs = field.deconstruct()
    assert kwargs['storage'] is storage_models.callable_storage

def test_deconstruct_preserves_storage_identity_for_instance_from_model_field():
    field = storage_models.Storage._meta.get_field('normal')
    _, _, _, kwargs = field.deconstruct()
    assert kwargs['storage'] is storage_models.temp_storage

import inspect
from pathlib import Path
import pytest
from django.core.files.storage import default_storage
from django.db.models.fields.files import FileField
from tests.file_storage import models as fm_models
from tests.file_storage.models import Storage

def test_deconstruct_callable_returns_default_storage_included():
    """
    If storage was provided as a callable that returns default_storage,
    deconstruct() must include the callable in kwargs['storage'].
    """
    field = Storage._meta.get_field('storage_callable_default')
    name, path, args, kwargs = field.deconstruct()
    assert 'storage' in kwargs
    assert kwargs['storage'] is fm_models.callable_default_storage

def test_deconstruct_callable_returns_custom_storage_included():
    """
    If storage was provided as a callable that returns a custom storage
    (temp_storage), deconstruct() must include the callable in kwargs['storage'].
    """
    field = Storage._meta.get_field('storage_callable')
    name, path, args, kwargs = field.deconstruct()
    assert 'storage' in kwargs
    assert kwargs['storage'] is fm_models.callable_storage

def test_deconstruct_storage_class_callable_included():
    """
    If storage was provided as a class (callable) that will be instantiated,
    deconstruct() must include the original callable/class in kwargs['storage'].
    """
    field = Storage._meta.get_field('storage_callable_class')
    name, path, args, kwargs = field.deconstruct()
    assert 'storage' in kwargs
    assert kwargs['storage'] is fm_models.CallableStorage

def test_deconstruct_storage_instance_included_when_not_default():
    """
    If storage was provided as a Storage instance that's not default_storage,
    deconstruct() must include that storage instance in kwargs.
    """
    field = Storage._meta.get_field('normal')
    name, path, args, kwargs = field.deconstruct()
    assert 'storage' in kwargs
    assert kwargs['storage'] is fm_models.temp_storage
    assert kwargs['upload_to'] == 'tests'
    assert 'max_length' not in kwargs

def test_deconstruct_default_storage_not_included():
    """
    If storage is the default_storage instance and not provided as a callable,
    deconstruct() must not include the 'storage' kwarg.
    """
    f = FileField(storage=default_storage, upload_to='x')
    name, path, args, kwargs = f.deconstruct()
    assert 'storage' not in kwargs

def test_deconstruct_preserves_pathlib_upload_to_direct():
    """
    When upload_to is a pathlib.Path instance, it should be preserved by deconstruct().
    """
    field = Storage._meta.get_field('pathlib_direct')
    name, path, args, kwargs = field.deconstruct()
    assert 'upload_to' in kwargs
    assert isinstance(kwargs['upload_to'], Path)
    assert kwargs['upload_to'] == Path('bar')

def test_deconstruct_preserves_callable_upload_to_that_returns_pathlib():
    """
    When upload_to is a callable that returns a Path, deconstruct should
    preserve the callable (not the returned Path).
    """
    field = Storage._meta.get_field('pathlib_callable')
    name, path, args, kwargs = field.deconstruct()
    assert 'upload_to' in kwargs
    assert kwargs['upload_to'] is Storage.pathlib_upload_to

def test_deconstruct_preserves_custom_callable_upload_to():
    """
    upload_to values that are callables (functions/methods) must be preserved.
    """
    field = Storage._meta.get_field('custom')
    name, path, args, kwargs = field.deconstruct()
    assert 'upload_to' in kwargs
    assert kwargs['upload_to'] is Storage.custom_upload_to

def test_deconstruct_max_length_behavior_for_explicit_values():
    """
    max_length is removed from kwargs when it's the default (100),
    but preserved when explicitly set to a different value.
    """
    limited = Storage._meta.get_field('limited_length')
    name, path, args, kwargs = limited.deconstruct()
    assert kwargs.get('max_length') == 20
    extended = Storage._meta.get_field('extended_length')
    name, path, args, kwargs = extended.deconstruct()
    assert kwargs.get('max_length') == 300
    normal = Storage._meta.get_field('normal')
    name, path, args, kwargs = normal.deconstruct()
    assert 'max_length' not in kwargs

def test_deconstruct_custom_storage_instance_is_preserved():
    """
    When a custom Storage instance (subclass instance) is provided, it should
    be preserved verbatim in the deconstructed kwargs.
    """
    field = Storage._meta.get_field('custom_valid_name')
    name, path, args, kwargs = field.deconstruct()
    assert 'storage' in kwargs
    assert kwargs['storage'].__class__ is fm_models.CustomValidNameStorage

import inspect
import pytest
from django.core.files.storage import default_storage
from django.db.models.fields.files import FileField
from tests.file_storage import models as fs_models

def _deconstruct_storage_value(field):
    """
    Helper: return the 'storage' value from deconstruct kwargs (or None if absent).
    """
    name, path, args, kwargs = field.deconstruct()
    return (kwargs.get('storage', None), kwargs)

def test_deconstruct_omits_default_storage_instance():
    f = FileField(storage=default_storage)
    storage_value, kwargs = _deconstruct_storage_value(f)
    assert 'storage' not in kwargs
    assert storage_value is None

def test_deconstruct_includes_custom_storage_instance():
    f = FileField(storage=fs_models.temp_storage)
    storage_value, kwargs = _deconstruct_storage_value(f)
    assert 'storage' in kwargs
    assert storage_value is fs_models.temp_storage

def test_deconstruct_includes_callable_returning_custom_storage():
    f = FileField(storage=fs_models.callable_storage, upload_to='tests')
    storage_value, kwargs = _deconstruct_storage_value(f)
    assert 'storage' in kwargs
    assert storage_value is fs_models.callable_storage
    assert callable(storage_value)
    assert storage_value() is fs_models.temp_storage

def test_deconstruct_includes_callable_returning_default_storage():
    f = FileField(storage=fs_models.callable_default_storage)
    storage_value, kwargs = _deconstruct_storage_value(f)
    assert 'storage' in kwargs
    assert storage_value is fs_models.callable_default_storage
    assert callable(storage_value)
    assert storage_value() is default_storage

def test_deconstruct_includes_callable_class():
    f = FileField(storage=fs_models.CallableStorage)
    storage_value, kwargs = _deconstruct_storage_value(f)
    assert 'storage' in kwargs
    assert storage_value is fs_models.CallableStorage
    instance = storage_value()
    assert hasattr(instance, 'location') or hasattr(instance, 'base_location') or inspect.isclass(storage_value) is False

def test_deconstruct_includes_callable_instance():
    instance = fs_models.CallableStorage()
    f = FileField(storage=instance)
    storage_value, kwargs = _deconstruct_storage_value(f)
    assert 'storage' in kwargs
    assert storage_value is instance

def test_model_field_deconstruct_callable_default_storage():
    field = fs_models.Storage._meta.get_field('storage_callable_default')
    storage_value, kwargs = _deconstruct_storage_value(field)
    assert 'storage' in kwargs
    assert storage_value is fs_models.callable_default_storage

def test_model_field_deconstruct_callable_custom_storage():
    field = fs_models.Storage._meta.get_field('storage_callable')
    storage_value, kwargs = _deconstruct_storage_value(field)
    assert 'storage' in kwargs
    assert storage_value is fs_models.callable_storage

def test_model_field_deconstruct_callable_class_preserved():
    field = fs_models.Storage._meta.get_field('storage_callable_class')
    storage_value, kwargs = _deconstruct_storage_value(field)
    assert 'storage' in kwargs
    assert storage_value is fs_models.CallableStorage

def test_deconstruct_preserves_identity_of_storage_callable_and_instance():
    func_field = FileField(storage=fs_models.callable_storage)
    func_storage_value, _ = _deconstruct_storage_value(func_field)
    assert func_storage_value is fs_models.callable_storage
    inst = fs_models.CallableStorage()
    inst_field = FileField(storage=inst)
    inst_storage_value, _ = _deconstruct_storage_value(inst_field)
    assert inst_storage_value is inst

import tempfile
from pathlib import Path
import pytest
from django.core.files.storage import FileSystemStorage, default_storage
from django.db.models import FileField
import tempfile
from pathlib import Path
import pytest
from django.core.files.storage import FileSystemStorage, default_storage
from django.db.models import FileField

def test_deconstruct_omits_default_storage_instance():
    f = FileField(upload_to='foo', storage=default_storage)
    name, path, args, kwargs = f.deconstruct()
    assert 'storage' not in kwargs

def test_deconstruct_includes_custom_storage_instance():
    tmpdir = tempfile.mkdtemp()
    fs = FileSystemStorage(location=tmpdir)
    f = FileField(upload_to='foo', storage=fs)
    name, path, args, kwargs = f.deconstruct()
    assert 'storage' in kwargs
    assert kwargs['storage'] is fs

def test_deconstruct_includes_callable_returning_custom_storage():
    tmpdir = tempfile.mkdtemp()
    fs = FileSystemStorage(location=tmpdir)

    def get_storage():
        return fs
    f = FileField(upload_to='foo', storage=get_storage)
    name, path, args, kwargs = f.deconstruct()
    assert 'storage' in kwargs
    assert kwargs['storage'] is get_storage

def test_deconstruct_includes_callable_returning_default_storage():

    def get_default_storage():
        return default_storage
    f = FileField(upload_to='foo', storage=get_default_storage)
    name, path, args, kwargs = f.deconstruct()
    assert 'storage' in kwargs
    assert kwargs['storage'] is get_default_storage

def test_deconstruct_includes_callable_storage_class():

    class MyCallableStorage(FileSystemStorage):

        def __call__(self):
            return self
    f = FileField(upload_to='foo', storage=MyCallableStorage)
    name, path, args, kwargs = f.deconstruct()
    assert 'storage' in kwargs
    assert kwargs['storage'] is MyCallableStorage

def test_deconstruct_removes_default_max_length():
    f = FileField(upload_to='foo')
    name, path, args, kwargs = f.deconstruct()
    assert 'max_length' not in kwargs

def test_deconstruct_keeps_nondefault_max_length():
    f = FileField(upload_to='foo', max_length=300)
    name, path, args, kwargs = f.deconstruct()
    assert 'max_length' in kwargs and kwargs['max_length'] == 300

def test_deconstruct_includes_upload_to_string():
    f = FileField(upload_to='bar')
    name, path, args, kwargs = f.deconstruct()
    assert 'upload_to' in kwargs and kwargs['upload_to'] == 'bar'

def test_deconstruct_includes_upload_to_callable():

    def my_upload(instance, filename):
        return 'x/' + filename
    f = FileField(upload_to=my_upload)
    name, path, args, kwargs = f.deconstruct()
    assert 'upload_to' in kwargs and kwargs['upload_to'] is my_upload

def test_deconstruct_includes_upload_to_pathlib():
    p = Path('baz')
    f = FileField(upload_to=p)
    name, path, args, kwargs = f.deconstruct()
    assert 'upload_to' in kwargs and kwargs['upload_to'] == p

import types
import pytest
from django.core.files.storage import default_storage
from django.db.models import FileField
from tests.file_storage import models as fs_models
import types
import pytest
from django.core.files.storage import default_storage
from django.db.models import FileField
from tests.file_storage import models as fs_models

def test_deconstruct_includes_storage_instance_non_default():
    field = fs_models.Storage._meta.get_field('normal')
    kwargs = _deconstruct_field(field)
    assert 'storage' in kwargs
    assert kwargs['storage'] is fs_models.temp_storage

def test_deconstruct_includes_storage_for_callable_function():
    field = fs_models.Storage._meta.get_field('storage_callable')
    kwargs = _deconstruct_field(field)
    assert 'storage' in kwargs
    assert kwargs['storage'] is fs_models.callable_storage

def test_deconstruct_includes_storage_for_callable_class():
    field = fs_models.Storage._meta.get_field('storage_callable_class')
    kwargs = _deconstruct_field(field)
    assert 'storage' in kwargs
    assert kwargs['storage'] is fs_models.CallableStorage

def test_deconstruct_includes_callable_even_if_it_returns_default_storage():
    field = fs_models.Storage._meta.get_field('storage_callable_default')
    kwargs = _deconstruct_field(field)
    assert 'storage' in kwargs
    assert kwargs['storage'] is fs_models.callable_default_storage

def test_deconstruct_excludes_default_storage_when_no_callable():
    f = FileField(storage=default_storage)
    kwargs = _deconstruct_field(f)
    assert 'storage' not in kwargs

def test_deconstruct_excludes_when__storage_callable_mutated_to_default_on_callable_default():
    field = fs_models.Storage._meta.get_field('storage_callable_default')
    field._storage_callable = default_storage
    kwargs = _deconstruct_field(field)
    assert 'storage' not in kwargs

def test_deconstruct_excludes_when__storage_callable_mutated_to_default_on_instance_storage():
    field = fs_models.Storage._meta.get_field('normal')
    field._storage_callable = default_storage
    kwargs = _deconstruct_field(field)
    assert 'storage' not in kwargs

def test_deconstruct_excludes_when__storage_callable_mutated_to_default_on_callable_class():
    field = fs_models.Storage._meta.get_field('storage_callable_class')
    field._storage_callable = default_storage
    kwargs = _deconstruct_field(field)
    assert 'storage' not in kwargs

def test_deconstruct_preserves_original_callable_object_identity():
    field = fs_models.Storage._meta.get_field('storage_callable_default')
    field._storage_callable = fs_models.callable_default_storage
    kwargs = _deconstruct_field(field)
    assert 'storage' in kwargs
    assert isinstance(kwargs['storage'], types.FunctionType)
    assert kwargs['storage'] is fs_models.callable_default_storage

def test_deconstruct_preserves_storage_instance_identity_for_temp_storage():
    field = fs_models.Storage._meta.get_field('normal')
    if hasattr(field, '_storage_callable'):
        delattr(field, '_storage_callable')
    kwargs = _deconstruct_field(field)
    assert 'storage' in kwargs
    assert kwargs['storage'] is fs_models.temp_storage

import tempfile
from pathlib import Path
import pytest
from django.core.files.storage import FileSystemStorage, default_storage
from django.db.models.fields.files import FileField
temp_location = tempfile.mkdtemp()
temp_storage = FileSystemStorage(location=temp_location)

def custom_storage_callable():
    return temp_storage

def default_storage_callable():
    return default_storage

def test_deconstruct_omits_default_storage_instance():
    f = FileField(storage=default_storage, upload_to='tests')
    name, path, args, kwargs = f.deconstruct()
    assert 'storage' not in kwargs
    assert kwargs['upload_to'] == 'tests'

def test_deconstruct_includes_custom_storage_instance():
    s = FileSystemStorage(location=temp_location)
    f = FileField(storage=s, upload_to='u')
    name, path, args, kwargs = f.deconstruct()
    assert 'storage' in kwargs
    assert kwargs['storage'] is s
    assert kwargs['upload_to'] == 'u'

def test_deconstruct_includes_callable_returning_custom_storage():
    f = FileField(storage=custom_storage_callable, upload_to='u2')
    name, path, args, kwargs = f.deconstruct()
    assert 'storage' in kwargs
    assert kwargs['storage'] is custom_storage_callable
    assert kwargs['upload_to'] == 'u2'

def test_deconstruct_includes_callable_returning_default_storage():
    f = FileField(storage=default_storage_callable, upload_to='u3')
    name, path, args, kwargs = f.deconstruct()
    assert 'storage' in kwargs
    assert kwargs['storage'] is default_storage_callable
    assert kwargs['upload_to'] == 'u3'

def test_deconstruct_includes_callable_class_storage():
    f = FileField(storage=CallableStorage, upload_to=Path('bar'))
    name, path, args, kwargs = f.deconstruct()
    assert 'storage' in kwargs
    assert kwargs['storage'] is CallableStorage
    assert kwargs['upload_to'] == Path('bar')

def test_deconstruct_preserves_callable_identity_for_default_callable_from_tests():

    def some_callable_default():
        return default_storage
    f = FileField(storage=some_callable_default, upload_to='u4')
    name, path, args, kwargs = f.deconstruct()
    assert 'storage' in kwargs
    assert kwargs['storage'] is some_callable_default
    assert kwargs['upload_to'] == 'u4'

def test_deconstruct_default_max_length_is_removed():
    f = FileField(storage=temp_storage, upload_to='u5')
    name, path, args, kwargs = f.deconstruct()
    assert 'max_length' not in kwargs
    f2 = FileField(storage=temp_storage, upload_to='u6', max_length=300)
    _, _, _, kwargs2 = f2.deconstruct()
    assert kwargs2.get('max_length') == 300

def test_deconstruct_mutated_storage_callable_set_to_default_omits_storage():
    """
    This test simulates a situation where the internal _storage_callable attribute
    exists but both the effective storage and the callable resolve to the
    default_storage. The intended behavior (gold patch) is that deconstruct()
    should not include a 'storage' kwarg when the effective storage is the
    default_storage instance. The candidate patch incorrectly bases inclusion
    on the mere presence of _storage_callable and therefore would include a
    'storage' kwarg in this scenario; that is what this test is designed to catch.
    """
    f = FileField(storage=default_storage_callable, upload_to='u7')
    f._storage_callable = default_storage
    f.storage = default_storage
    name, path, args, kwargs = f.deconstruct()
    assert 'storage' not in kwargs

def test_deconstruct_storage_callable_preserved_when_returning_custom_storage_instance():

    def make_new_storage():
        return FileSystemStorage(location=temp_location)
    f = FileField(storage=make_new_storage, upload_to='u8')
    name, path, args, kwargs = f.deconstruct()
    assert 'storage' in kwargs
    assert kwargs['storage'] is make_new_storage

from tests.file_storage import models as storage_models
from django.db.models.fields.files import FileField
import inspect
import pytest
from django.core.files.storage import default_storage
from django.db.models.fields.files import FileField
from tests.file_storage import models as storage_models

def test_normal_storage_included_and_matches_temp_storage():
    field = storage_models.Storage._meta.get_field('normal')
    name, path, args, kwargs = field.deconstruct()
    assert 'storage' in kwargs, 'storage should be included for non-default storage instances'
    assert kwargs['storage'] is storage_models.temp_storage

def test_default_storage_not_included_in_deconstruct():
    f = FileField(upload_to='uploads')
    name, path, args, kwargs = f.deconstruct()
    assert 'storage' not in kwargs, 'default_storage should not be included in deconstruction'

def test_callable_storage_function_included_as_callable():
    field = storage_models.Storage._meta.get_field('storage_callable')
    name, path, args, kwargs = field.deconstruct()
    assert 'storage' in kwargs
    assert kwargs['storage'] is storage_models.callable_storage
    assert callable(kwargs['storage'])

def test_callable_storage_class_included_as_class():
    field = storage_models.Storage._meta.get_field('storage_callable_class')
    name, path, args, kwargs = field.deconstruct()
    assert 'storage' in kwargs
    assert kwargs['storage'] is storage_models.CallableStorage
    assert callable(kwargs['storage'])

def test_callable_returning_default_storage_included_as_callable():
    field = storage_models.Storage._meta.get_field('storage_callable_default')
    name, path, args, kwargs = field.deconstruct()
    assert 'storage' in kwargs
    assert kwargs['storage'] is storage_models.callable_default_storage
    assert callable(kwargs['storage'])
    assert kwargs['storage']() is default_storage

def test_custom_storage_instance_included_and_matches_instance():
    field = storage_models.Storage._meta.get_field('custom_valid_name')
    name, path, args, kwargs = field.deconstruct()
    assert 'storage' in kwargs
    assert kwargs['storage'] is storage_models.CustomValidNameStorage(location=storage_models.temp_storage_location) or isinstance(kwargs['storage'], storage_models.CustomValidNameStorage.__mro__[0].__class__)
    assert isinstance(kwargs['storage'], type(storage_models.temp_storage))

def test_reconstruct_roundtrip_for_instance_storage():
    original = storage_models.Storage._meta.get_field('normal')
    name, path, args, kwargs = original.deconstruct()
    new_field = FileField(*args, **kwargs)
    assert 'storage' in kwargs
    assert new_field.storage is storage_models.temp_storage

def test_reconstruct_roundtrip_for_callable_storage_function():
    original = storage_models.Storage._meta.get_field('storage_callable')
    name, path, args, kwargs = original.deconstruct()
    assert 'storage' in kwargs
    new_field = FileField(*args, **kwargs)
    assert hasattr(new_field, '_storage_callable')
    assert new_field._storage_callable is storage_models.callable_storage
    assert new_field.storage is storage_models.temp_storage

def test_reconstruct_roundtrip_for_callable_returning_default_storage():
    original = storage_models.Storage._meta.get_field('storage_callable_default')
    name, path, args, kwargs = original.deconstruct()
    assert 'storage' in kwargs
    new_field = FileField(*args, **kwargs)
    assert hasattr(new_field, '_storage_callable')
    assert new_field._storage_callable is storage_models.callable_default_storage
    assert new_field.storage is default_storage

def test_reconstruct_roundtrip_for_callable_class_storage():
    original = storage_models.Storage._meta.get_field('storage_callable_class')
    name, path, args, kwargs = original.deconstruct()
    assert 'storage' in kwargs
    new_field = FileField(*args, **kwargs)
    assert hasattr(new_field, '_storage_callable')
    assert new_field._storage_callable is storage_models.CallableStorage
    assert isinstance(new_field.storage, storage_models.CallableStorage)

import tempfile
from pathlib import Path
from django.core.files.storage import FileSystemStorage, default_storage
from django.db.models.fields.files import FileField
temp_storage_location = tempfile.mkdtemp()
temp_storage = FileSystemStorage(location=temp_storage_location)

def callable_storage():
    return temp_storage

def callable_default_storage():
    return default_storage

def test_deconstruct_includes_storage_instance():
    f = FileField(storage=temp_storage, upload_to='tests')
    name, path, args, kwargs = f.deconstruct()
    assert 'storage' in kwargs
    assert kwargs['storage'] is temp_storage

def test_deconstruct_includes_storage_callable_function():
    f = FileField(storage=callable_storage, upload_to='storage_callable')
    name, path, args, kwargs = f.deconstruct()
    assert 'storage' in kwargs
    assert kwargs['storage'] is callable_storage

def test_deconstruct_includes_callable_even_if_it_returns_default_storage():
    f = FileField(storage=callable_default_storage, upload_to='storage_callable_default')
    name, path, args, kwargs = f.deconstruct()
    assert 'storage' in kwargs
    assert kwargs['storage'] is callable_default_storage

def test_deconstruct_includes_callable_class():
    f = FileField(storage=CallableStorageClass, upload_to='storage_callable_class')
    name, path, args, kwargs = f.deconstruct()
    assert 'storage' in kwargs
    assert kwargs['storage'] is CallableStorageClass

def test_deconstruct_omits_storage_when_default_and_not_callable():
    f = FileField(upload_to='tests')
    name, path, args, kwargs = f.deconstruct()
    assert 'storage' not in kwargs

def test_deconstruct_omits_storage_when_explicit_default_storage_passed():
    f = FileField(storage=default_storage, upload_to='tests')
    name, path, args, kwargs = f.deconstruct()
    assert 'storage' not in kwargs

def test_deconstruct_omits_default_max_length():
    f = FileField(upload_to='tests')
    name, path, args, kwargs = f.deconstruct()
    assert 'max_length' not in kwargs

def test_deconstruct_preserves_non_default_max_length():
    f = FileField(upload_to='tests', max_length=300, storage=temp_storage)
    name, path, args, kwargs = f.deconstruct()
    assert 'max_length' in kwargs
    assert kwargs['max_length'] == 300

def test_deconstruct_preserves_callable_upload_to():

    def my_upload_to(instance, filename):
        return 'foo/%s' % filename
    f = FileField(upload_to=my_upload_to, storage=temp_storage)
    name, path, args, kwargs = f.deconstruct()
    assert 'upload_to' in kwargs
    assert kwargs['upload_to'] is my_upload_to

def test_deconstruct_preserves_pathlib_upload_to():
    p = Path('bar')
    f = FileField(upload_to=p, storage=temp_storage)
    name, path, args, kwargs = f.deconstruct()
    assert 'upload_to' in kwargs
    assert kwargs['upload_to'] == p

from tests.file_storage import models as fs_models
import inspect
from django.core.files.storage import default_storage
from django.db.models.fields.files import FileField
from tests.file_storage import models as fs_models

def test_deconstruct_with_explicit_storage_instance_included():
    field = FileField(storage=fs_models.temp_storage, upload_to='tests')
    name, path, args, kwargs = field.deconstruct()
    assert 'storage' in kwargs
    assert kwargs['storage'] is fs_models.temp_storage

def test_deconstruct_with_default_storage_omitted():
    field = FileField(storage=default_storage, upload_to='tests')
    name, path, args, kwargs = field.deconstruct()
    assert 'storage' not in kwargs

def test_deconstruct_with_callable_returning_instance_includes_callable():
    field = FileField(storage=fs_models.callable_storage, upload_to='tests')
    name, path, args, kwargs = field.deconstruct()
    assert 'storage' in kwargs
    assert kwargs['storage'] is fs_models.callable_storage

def test_deconstruct_with_callable_returning_default_includes_callable():
    field = FileField(storage=fs_models.callable_default_storage, upload_to='tests')
    name, path, args, kwargs = field.deconstruct()
    assert 'storage' in kwargs
    assert kwargs['storage'] is fs_models.callable_default_storage

def test_deconstruct_with_callable_class_includes_callable_class():
    field = FileField(storage=fs_models.CallableStorage, upload_to='tests')
    name, path, args, kwargs = field.deconstruct()
    assert 'storage' in kwargs
    assert kwargs['storage'] is fs_models.CallableStorage

def test_deconstruct_model_field_with_instance_storage_included():
    field = fs_models.Storage._meta.get_field('normal')
    name, path, args, kwargs = field.deconstruct()
    assert 'storage' in kwargs
    assert kwargs['storage'] is fs_models.temp_storage

def test_deconstruct_model_field_with_callable_storage_includes_callable():
    field = fs_models.Storage._meta.get_field('storage_callable')
    name, path, args, kwargs = field.deconstruct()
    assert 'storage' in kwargs
    assert kwargs['storage'] is fs_models.callable_storage

def test_deconstruct_model_field_with_callable_class_includes_callable_class():
    field = fs_models.Storage._meta.get_field('storage_callable_class')
    name, path, args, kwargs = field.deconstruct()
    assert 'storage' in kwargs
    assert kwargs['storage'] is fs_models.CallableStorage

def test_deconstruct_model_field_with_callable_default_includes_callable():
    field = fs_models.Storage._meta.get_field('storage_callable_default')
    name, path, args, kwargs = field.deconstruct()
    assert 'storage' in kwargs
    assert kwargs['storage'] is fs_models.callable_default_storage

def test_deconstruct_omits_default_max_length_and_preserves_upload_to():
    field = FileField(upload_to='my_uploads')
    name, path, args, kwargs = field.deconstruct()
    assert 'max_length' not in kwargs
    assert kwargs.get('upload_to') == 'my_uploads'

from tests.file_storage import models as fs_models
import types
from pathlib import Path
import pytest
from django.core.files.storage import default_storage
from django.db.models.fields.files import FileField
from tests.file_storage import models as fs_models

def _deconstruct_kwargs(field):
    return field.deconstruct()[3]

def test_instance_storage_included():
    field = fs_models.Storage._meta.get_field('normal')
    kwargs = _deconstruct_kwargs(field)
    assert 'storage' in kwargs
    assert kwargs['storage'] is fs_models.temp_storage

def test_callable_storage_included_as_callable():
    field = fs_models.Storage._meta.get_field('storage_callable')
    kwargs = _deconstruct_kwargs(field)
    assert 'storage' in kwargs
    assert kwargs['storage'] is fs_models.callable_storage
    assert isinstance(kwargs['storage'], types.FunctionType)

def test_callable_class_storage_included_as_class():
    field = fs_models.Storage._meta.get_field('storage_callable_class')
    kwargs = _deconstruct_kwargs(field)
    assert 'storage' in kwargs
    assert kwargs['storage'] is fs_models.CallableStorage
    assert isinstance(kwargs['storage'], type)

def test_callable_returning_default_included_as_callable():
    field = fs_models.Storage._meta.get_field('storage_callable_default')
    kwargs = _deconstruct_kwargs(field)
    assert 'storage' in kwargs
    assert kwargs['storage'] is fs_models.callable_default_storage
    assert kwargs['storage']() is default_storage

def test_default_storage_excluded():
    field = FileField(storage=default_storage)
    kwargs = _deconstruct_kwargs(field)
    assert 'storage' not in kwargs

def test_max_length_default_removed():
    field = FileField(upload_to='tests', max_length=100)
    kwargs = _deconstruct_kwargs(field)
    assert 'max_length' not in kwargs

def test_pathlib_upload_to_preserved():
    field = fs_models.Storage._meta.get_field('pathlib_direct')
    kwargs = _deconstruct_kwargs(field)
    assert 'upload_to' in kwargs
    assert kwargs['upload_to'] == Path('bar')
    assert isinstance(kwargs['upload_to'], Path)

def test_manual_storage_callable_set_to_default_storage_excluded():
    field = FileField(storage=default_storage)
    field._storage_callable = default_storage
    kwargs = _deconstruct_kwargs(field)
    assert 'storage' not in kwargs

def test_custom_storage_instance_included():
    field = fs_models.Storage._meta.get_field('custom_valid_name')
    kwargs = _deconstruct_kwargs(field)
    assert 'storage' in kwargs
    storage_obj = kwargs['storage']
    assert storage_obj.__class__ is fs_models.CustomValidNameStorage
    assert getattr(storage_obj, 'location', None) == fs_models.temp_storage_location

def test_callable_instance_storage_included():
    inst = fs_models.CallableStorage()
    field = FileField(storage=inst)
    kwargs = _deconstruct_kwargs(field)
    assert 'storage' in kwargs
    assert kwargs['storage'] is inst

from pathlib import Path
import types
from pathlib import Path
from django.db.models.fields.files import FileField
from tests.file_storage import models as m
from django.core.files.storage import default_storage

def test_deconstruct_includes_callable_returning_default_storage():
    """
    If storage was provided as a callable that returns default_storage,
    the callable itself must be included in deconstruct() kwargs.
    """
    field = m.Storage._meta.get_field('storage_callable_default')
    name, path, args, kwargs = field.deconstruct()
    assert 'storage' in kwargs
    assert kwargs['storage'] is m.callable_default_storage
    assert callable(kwargs['storage'])

def test_deconstruct_includes_callable_returning_temp_storage():
    """
    If storage was provided as a callable that returns a non-default storage,
    the callable itself must be included in deconstruct() kwargs.
    """
    field = m.Storage._meta.get_field('storage_callable')
    name, path, args, kwargs = field.deconstruct()
    assert 'storage' in kwargs
    assert kwargs['storage'] is m.callable_storage
    assert callable(kwargs['storage'])

def test_deconstruct_includes_storage_instance():
    """
    If storage was provided as an explicit Storage instance (non-default),
    it should be present in deconstruct() kwargs.
    """
    field = m.Storage._meta.get_field('normal')
    name, path, args, kwargs = field.deconstruct()
    assert 'storage' in kwargs
    assert kwargs['storage'] is m.temp_storage

def test_deconstruct_includes_callable_class():
    """
    If a storage class (callable) was provided, the class itself should be
    preserved in deconstruction (so migrations can re-instantiate it).
    """
    field = m.Storage._meta.get_field('storage_callable_class')
    name, path, args, kwargs = field.deconstruct()
    assert 'storage' in kwargs
    assert kwargs['storage'] is m.CallableStorage
    assert isinstance(kwargs['storage'], type)

def test_deconstruct_excludes_default_storage_when_not_specified():
    """
    If no storage kwarg was provided (default_storage is used), deconstruct()
    must not include a 'storage' kwarg.
    """
    ff = FileField()
    name, path, args, kwargs = ff.deconstruct()
    assert 'storage' not in kwargs

def test_deconstruct_removes_default_max_length():
    """
    The default max_length (100) should not be included in deconstruction.
    """
    field = m.Storage._meta.get_field('normal')
    name, path, args, kwargs = field.deconstruct()
    assert 'max_length' not in kwargs

def test_deconstruct_preserves_non_default_max_length():
    """
    A user-specified max_length should be preserved in deconstruction.
    """
    field = m.Storage._meta.get_field('limited_length')
    name, path, args, kwargs = field.deconstruct()
    assert kwargs.get('max_length') == 20

def test_deconstruct_preserves_upload_to_callable_and_pathlib():
    """
    Ensure upload_to values are preserved as provided: callables remain
    callables and Path objects remain Path objects.
    """
    field_callable = m.Storage._meta.get_field('custom')
    name, path, args, kwargs = field_callable.deconstruct()
    assert kwargs['upload_to'] is m.Storage.custom_upload_to
    field_pathlib = m.Storage._meta.get_field('pathlib_direct')
    name, path, args, kwargs = field_pathlib.deconstruct()
    assert kwargs['upload_to'] == Path('bar')

def test_deconstruct_preserves_custom_storage_subclass_instance():
    """
    When a custom Storage instance (subclass) is provided, it should be
    preserved in deconstruction and be the same type.
    """
    field = m.Storage._meta.get_field('custom_valid_name')
    name, path, args, kwargs = field.deconstruct()
    assert 'storage' in kwargs
    assert type(kwargs['storage']).__name__ == 'CustomValidNameStorage'
    assert getattr(kwargs['storage'], 'location', None) == m.temp_storage_location

def test_deconstruct_storage_callable_is_callable_and_not_default_result():
    """
    Extra sanity: ensure the deconstructed storage for callable-based fields
    is the callable itself (not the result of calling it).
    """
    field = m.Storage._meta.get_field('storage_callable_default')
    name, path, args, kwargs = field.deconstruct()
    storage_val = kwargs['storage']
    assert isinstance(storage_val, types.FunctionType)
    assert storage_val is m.callable_default_storage

import tempfile
from pathlib import Path
from django.core.files.storage import FileSystemStorage, default_storage
from django.db.models.fields.files import FileField
import tempfile
from pathlib import Path
from django.core.files.storage import FileSystemStorage, default_storage
from django.db.models.fields.files import FileField
import types
temp_dir = tempfile.mkdtemp()
temp_storage = FileSystemStorage(location=temp_dir)

def callable_temp_storage():
    return temp_storage
f_default_instance = FileField(upload_to='uploads', storage=default_storage)
name, path, args, kwargs = f_default_instance.deconstruct()
assert 'storage' not in kwargs, 'default_storage instance should not be included in deconstruct kwargs'
f_custom_instance = FileField(upload_to='uploads', storage=temp_storage)
name, path, args, kwargs = f_custom_instance.deconstruct()
assert 'storage' in kwargs, 'custom storage instance should be included in deconstruct kwargs'
assert kwargs['storage'] is temp_storage
f_callable_custom = FileField(upload_to='uploads', storage=callable_temp_storage)
name, path, args, kwargs = f_callable_custom.deconstruct()
assert 'storage' in kwargs, 'callable custom storage should be included in deconstruct kwargs'
assert kwargs['storage'] is callable_temp_storage
f_callable_default = FileField(upload_to='uploads', storage=callable_default_storage)
name, path, args, kwargs = f_callable_default.deconstruct()
assert 'storage' in kwargs, 'callable returning default_storage must still be included in kwargs'
assert kwargs['storage'] is callable_default_storage
f_callable_class = FileField(upload_to='uploads', storage=CallableStorageClass)
name, path, args, kwargs = f_callable_class.deconstruct()
assert 'storage' in kwargs, 'callable storage class must be included in kwargs'
assert kwargs['storage'] is CallableStorageClass
f_default_max = FileField(upload_to='uploads')
name, path, args, kwargs = f_default_max.deconstruct()
assert 'max_length' not in kwargs, 'default max_length of 100 should be omitted from deconstruct kwargs'
f_explicit_max = FileField(upload_to='uploads', max_length=255)
name, path, args, kwargs = f_explicit_max.deconstruct()
assert 'max_length' in kwargs and kwargs['max_length'] == 255
f_upload_str = FileField(upload_to='my_uploads', storage=temp_storage)
name, path, args, kwargs = f_upload_str.deconstruct()
assert kwargs['upload_to'] == 'my_uploads'

def upload_callable(instance, filename):
    return Path('foo') / filename
f_upload_callable = FileField(upload_to=upload_callable, storage=temp_storage)
name, path, args, kwargs = f_upload_callable.deconstruct()
assert kwargs['upload_to'] is upload_callable
f_upload_pathlib = FileField(upload_to=Path('bar'), storage=temp_storage)
name, path, args, kwargs = f_upload_pathlib.deconstruct()
assert kwargs['upload_to'] == Path('bar')

import types
import pytest
from django.core.files.storage import default_storage
from django.db.models.fields.files import FileField
from tests.file_storage import models as storage_models
from tests.file_storage.models import callable_storage, callable_default_storage, CallableStorage, temp_storage

def _deconstruct_field(field):
    """
    Helper to call deconstruct on a field instance and return the kwargs dict.
    """
    name, path, args, kwargs = field.deconstruct()
    return kwargs

def test_deconstruct_includes_callable_returning_default_storage():
    """
    If a FileField was constructed with a callable that returns default_storage,
    deconstruct() must include the original callable (so migrations can
    re-create the same callable), not omit 'storage' because the resolved
    storage is default_storage.
    """
    field = storage_models.Storage._meta.get_field('storage_callable_default')
    kwargs = _deconstruct_field(field)
    assert 'storage' in kwargs
    assert kwargs['storage'] is callable_default_storage

def test_deconstruct_includes_callable_returning_custom_storage():
    """
    If a FileField was constructed with a callable that returns a custom
    storage, deconstruct() must include the callable.
    """
    field = storage_models.Storage._meta.get_field('storage_callable')
    kwargs = _deconstruct_field(field)
    assert 'storage' in kwargs
    assert kwargs['storage'] is callable_storage

def test_deconstruct_includes_callable_class_storage():
    """
    If a FileField was constructed with a callable class (CallableStorage),
    deconstruct() must include the original callable class object.
    """
    field = storage_models.Storage._meta.get_field('storage_callable_class')
    kwargs = _deconstruct_field(field)
    assert 'storage' in kwargs
    assert kwargs['storage'] is CallableStorage

def test_deconstruct_includes_storage_instance_when_non_default_storage_instance_provided():
    """
    If a FileField was constructed with a non-default storage instance,
    deconstruct() must include that storage instance.
    """
    field = storage_models.Storage._meta.get_field('normal')
    kwargs = _deconstruct_field(field)
    assert 'storage' in kwargs
    assert kwargs['storage'] is temp_storage

def test_deconstruct_does_not_include_storage_when_default_storage_passed_directly():
    """
    If a FileField was constructed with default_storage directly (not via
    a callable), deconstruct() should NOT include the storage kwarg.
    """
    field = FileField()
    assert getattr(field, 'storage', None) is default_storage
    kwargs = _deconstruct_field(field)
    assert 'storage' not in kwargs

def test_deconstruct_includes_storage_for_field_defined_without_upload_to_but_custom_storage():
    """
    Even if upload_to isn't set, a FileField with a custom storage instance
    should include storage in deconstruction. Use the 'empty' field which was
    created with temp_storage in the fixtures.
    """
    field = storage_models.Storage._meta.get_field('empty')
    kwargs = _deconstruct_field(field)
    assert 'storage' in kwargs
    assert kwargs['storage'] is temp_storage

def test_deconstruct_preserves_callable_identity_for_callable_that_returns_default_storage():
    """
    Ensure that the exact callable object used to construct the field is returned
    by deconstruct() for fields whose storage callable returns default_storage.
    """
    field = storage_models.Storage._meta.get_field('storage_callable_default')
    kwargs = _deconstruct_field(field)
    assert isinstance(kwargs['storage'], types.FunctionType)
    assert kwargs['storage'].__name__ == callable_default_storage.__name__
    assert kwargs['storage'] is callable_default_storage

def test_deconstruct_preserves_callable_identity_for_callable_that_returns_custom_storage():
    """
    Ensure that the exact callable object used to construct the field is returned
    by deconstruct() for fields whose storage callable returns a custom storage.
    """
    field = storage_models.Storage._meta.get_field('storage_callable')
    kwargs = _deconstruct_field(field)
    assert isinstance(kwargs['storage'], types.FunctionType)
    assert kwargs['storage'] is callable_storage

def test_deconstruct_includes_callable_for_pathlib_and_other_upload_variants():
    """
    Sanity check: deconstruct() should still include storage for a variety of
    other fields defined in the Storage model that explicitly set storage.
    """
    for fname in ('pathlib_callable', 'pathlib_direct', 'random', 'custom_valid_name'):
        field = storage_models.Storage._meta.get_field(fname)
        kwargs = _deconstruct_field(field)
        assert 'storage' in kwargs
        assert kwargs['storage'] is not default_storage

def test_deconstruct_includes_storage_callable_class_even_when_instance_equals_default_storage():
    """
    Edge case: if a callable was provided that happens to produce an instance
    which is equal (==) to default_storage but the original argument was a
    callable, deconstruct should include the callable. This reproduces the
    real-world scenario where a callable returns default_storage; the
    important behavior is to preserve the original callable argument.
    """
    field = storage_models.Storage._meta.get_field('storage_callable_default')
    kwargs = _deconstruct_field(field)
    assert 'storage' in kwargs
    assert kwargs['storage'] is callable_default_storage