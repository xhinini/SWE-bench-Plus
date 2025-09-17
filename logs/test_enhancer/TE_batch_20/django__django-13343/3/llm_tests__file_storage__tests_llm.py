import functools
import types
from django.test import SimpleTestCase
from django.db.models import FileField
from django.core.files.storage import default_storage
import functools
import types

class FileFieldDeconstructCallableDefaultStorageTests(SimpleTestCase):
    def test_function_returning_default_storage_omitted_from_deconstruct(self):
        def get_default_storage():
            return default_storage
        field = FileField(storage=get_default_storage)
        _, _, _, kwargs = field.deconstruct()
        self.assertNotIn('storage', kwargs)

    def test_lambda_returning_default_storage_omitted_from_deconstruct(self):
        get_default = lambda: default_storage
        field = FileField(storage=get_default)
        _, _, _, kwargs = field.deconstruct()
        self.assertNotIn('storage', kwargs)

    def test_nested_function_returning_default_storage_omitted_from_deconstruct(self):
        def outer():
            def inner():
                return default_storage
            return inner
        get_default = outer()
        field = FileField(storage=get_default)
        _, _, _, kwargs = field.deconstruct()
        self.assertNotIn('storage', kwargs)

    def test_bound_method_returning_default_storage_omitted_from_deconstruct(self):
        class Getter:
            def get(self):
                return default_storage
        g = Getter()
        field = FileField(storage=g.get)  # bound method
        _, _, _, kwargs = field.deconstruct()
        self.assertNotIn('storage', kwargs)

    def test_functor_instance_returning_default_storage_omitted_from_deconstruct(self):
        class Functor:
            def __call__(self):
                return default_storage
        f = Functor()
        field = FileField(storage=f)
        _, _, _, kwargs = field.deconstruct()
        self.assertNotIn('storage', kwargs)

    def test_partial_function_returning_default_storage_omitted_from_deconstruct(self):
        def get_default(x=None):
            return default_storage
        p = functools.partial(get_default, 1)
        field = FileField(storage=p)
        _, _, _, kwargs = field.deconstruct()
        self.assertNotIn('storage', kwargs)

    def test_types_methodtype_returning_default_storage_omitted_from_deconstruct(self):
        class Getter:
            def get(self):
                return default_storage
        g = Getter()
        bound = types.MethodType(Getter.get, g)
        field = FileField(storage=bound)
        _, _, _, kwargs = field.deconstruct()
        self.assertNotIn('storage', kwargs)

    def test_closure_returning_default_storage_omitted_from_deconstruct(self):
        def make_getter():
            val = default_storage
            def getter():
                return val
            return getter
        getter = make_getter()
        field = FileField(storage=getter)
        _, _, _, kwargs = field.deconstruct()
        self.assertNotIn('storage', kwargs)

    def test_partial_of_functor_returning_default_storage_omitted_from_deconstruct(self):
        class Functor:
            def __call__(self, *args, **kwargs):
                return default_storage
        f = Functor()
        p = functools.partial(f, 42)
        field = FileField(storage=p)
        _, _, _, kwargs = field.deconstruct()
        self.assertNotIn('storage', kwargs)

    def test_nested_partial_and_callable_returning_default_storage_omitted_from_deconstruct(self):
        def get_default(x, y=2):
            return default_storage
        p1 = functools.partial(get_default, 1)
        p2 = functools.partial(p1, y=2)
        field = FileField(storage=p2)
        _, _, _, kwargs = field.deconstruct()
        self.assertNotIn('storage', kwargs)

from functools import partial
import tempfile
from django.test import SimpleTestCase
from django.core.files.storage import FileSystemStorage, default_storage
from django.db.models import FileField
from functools import partial
import tempfile
from django.test import SimpleTestCase
from django.core.files.storage import FileSystemStorage, default_storage
from django.db.models import FileField

class FileFieldStorageCallableAttributeTests(SimpleTestCase):

    def test_callable_function_sets__storage_callable_attribute(self):

        def get_storage():
            return default_storage
        field = FileField(storage=get_storage)
        self.assertTrue(hasattr(field, '_storage_callable'))
        self.assertIs(field._storage_callable, get_storage)

    def test_callable_class_sets__storage_callable_attribute(self):
        field = FileField(storage=FileSystemStorage)
        self.assertTrue(hasattr(field, '_storage_callable'))
        self.assertIs(field._storage_callable, FileSystemStorage)

    def test_callable_instance_sets__storage_callable_attribute(self):

        class CallableObj:

            def __call__(self):
                return default_storage
        callable_obj = CallableObj()
        field = FileField(storage=callable_obj)
        self.assertTrue(hasattr(field, '_storage_callable'))
        self.assertIs(field._storage_callable, callable_obj)

    def test_lambda_sets__storage_callable_attribute(self):
        loader = lambda: default_storage
        field = FileField(storage=loader)
        self.assertTrue(hasattr(field, '_storage_callable'))
        self.assertIs(field._storage_callable, loader)

    def test_partial_sets__storage_callable_attribute(self):
        loader_partial = partial(lambda: default_storage)
        field = FileField(storage=loader_partial)
        self.assertTrue(hasattr(field, '_storage_callable'))
        self.assertIs(field._storage_callable, loader_partial)

from django.core.files.storage import FileSystemStorage, default_storage
from django.db.models import FileField
import unittest
from django.test import SimpleTestCase
from django.core.files.storage import FileSystemStorage, default_storage
from django.db.models import FileField

class FileFieldStorageCallableRegressionTests(SimpleTestCase):

    def test_callable_function_sets__storage_callable(self):

        def get_storage():
            return FileSystemStorage()
        f = FileField(storage=get_storage)
        self.assertTrue(hasattr(f, '_storage_callable'))
        self.assertIs(f._storage_callable, get_storage)

    def test_callable_class_sets__storage_callable(self):

        class GetStorage(FileSystemStorage):
            pass
        f = FileField(storage=GetStorage)
        self.assertTrue(hasattr(f, '_storage_callable'))
        self.assertIs(f._storage_callable, GetStorage)

    def test_invalid_returning_callable_sets__storage_callable_even_on_error(self):

        def get_invalid_storage():
            return object()
        f = FileField.__new__(FileField)
        with self.assertRaises(TypeError):
            FileField.__init__(f, storage=get_invalid_storage)
        self.assertTrue(hasattr(f, '_storage_callable'))
        self.assertIs(f._storage_callable, get_invalid_storage)

    def test_raising_callable_sets__storage_callable_even_on_error(self):

        def raising_storage():
            raise RuntimeError('boom')
        f = FileField.__new__(FileField)
        with self.assertRaises(RuntimeError):
            FileField.__init__(f, storage=raising_storage)
        self.assertTrue(hasattr(f, '_storage_callable'))
        self.assertIs(f._storage_callable, raising_storage)

    def test_callable_object_sets__storage_callable_and_deconstruct_returns_it(self):

        class CallableObj:

            def __call__(self):
                return FileSystemStorage()
        callable_obj = CallableObj()
        f = FileField(storage=callable_obj)
        self.assertTrue(hasattr(f, '_storage_callable'))
        self.assertIs(f._storage_callable, callable_obj)
        _, _, _, kwargs = f.deconstruct()
        self.assertIn('storage', kwargs)
        self.assertIs(kwargs['storage'], callable_obj)

from functools import partial
from functools import partial
import tempfile
import shutil
from django.test import SimpleTestCase
from django.core.files.storage import default_storage, FileSystemStorage
from django.db.models.fields.files import FileField

class FileFieldDeconstructTests(SimpleTestCase):

    def test_callable_returns_default_storage_deconstruct_omits_storage(self):

        def get_default():
            return default_storage
        name, path, args, kwargs = FileField(storage=get_default).deconstruct()
        self.assertNotIn('storage', kwargs)

    def test_lambda_returns_default_storage_omits_storage(self):
        storage_func = lambda: default_storage
        name, path, args, kwargs = FileField(storage=storage_func).deconstruct()
        self.assertNotIn('storage', kwargs)

    def test_partial_callable_returns_default_storage_omits_storage(self):
        storage_partial = partial(lambda x: x, default_storage)
        name, path, args, kwargs = FileField(storage=storage_partial).deconstruct()
        self.assertNotIn('storage', kwargs)

    def test_callable_class_returns_default_storage_omits_storage(self):

        class GetDefault:

            def __call__(self):
                return default_storage
        inst = GetDefault()
        name, path, args, kwargs = FileField(storage=inst).deconstruct()
        self.assertNotIn('storage', kwargs)

    def test_callable_wrapper_returning_default_storage_omits_storage(self):

        def wrapper():
            return default_storage
        name, path, args, kwargs = FileField(storage=wrapper).deconstruct()
        self.assertNotIn('storage', kwargs)

    def test_callable_returning_default_storage_vs_nondefault_behavior(self):
        tempdir = tempfile.mkdtemp()
        try:

            def get_default():
                return default_storage

            def get_fs():
                return FileSystemStorage(location=tempdir)
            _, _, _, kwargs_default = FileField(storage=get_default).deconstruct()
            _, _, _, kwargs_fs = FileField(storage=get_fs).deconstruct()
            self.assertNotIn('storage', kwargs_default)
            self.assertIn('storage', kwargs_fs)
            self.assertIs(kwargs_fs['storage'], get_fs)
        finally:
            shutil.rmtree(tempdir)