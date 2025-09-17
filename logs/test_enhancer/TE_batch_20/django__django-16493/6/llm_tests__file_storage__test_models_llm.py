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