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