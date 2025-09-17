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