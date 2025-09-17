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

import shutil
import tempfile
import types
from django.core.files.storage import FileSystemStorage, default_storage
from django.db.models import FileField
from django.test import SimpleTestCase
import shutil
import tempfile
import types
from django.core.files.storage import FileSystemStorage, default_storage
from django.db.models import FileField
from django.test import SimpleTestCase

class FileFieldDeconstructionTests(SimpleTestCase):

    def test_deconstruct_omits_storage_when_callable_returns_default_storage(self):

        def returns_default():
            return default_storage
        field = FileField(storage=returns_default)
        *_, kwargs = field.deconstruct()
        self.assertNotIn('storage', kwargs)

    def test_callable_object_returning_default_storage_omits_storage(self):

        class CallableReturnDefault:

            def __call__(self):
                return default_storage
        field = FileField(storage=CallableReturnDefault())
        *_, kwargs = field.deconstruct()
        self.assertNotIn('storage', kwargs)

    def test_lambda_callable_returns_default_storage_omits_storage(self):
        get_default = lambda: default_storage
        field = FileField(storage=get_default)
        *_, kwargs = field.deconstruct()
        self.assertNotIn('storage', kwargs)

import tempfile
from django.core.files.storage import FileSystemStorage
from django.test import SimpleTestCase
from django.db.models import FileField
from .models import callable_storage, Storage

class FileFieldStorageCallableAttributeTests(SimpleTestCase):

    def test_callable_function_sets__storage_callable_attribute(self):

        def get_storage():
            return FileSystemStorage()
        field = FileField(storage=get_storage)
        self.assertTrue(hasattr(field, '_storage_callable'))
        self.assertIs(field._storage_callable, get_storage)

    def test_callable_class_sets__storage_callable_attribute(self):

        class GetStorage(FileSystemStorage):
            pass
        field = FileField(storage=GetStorage)
        self.assertTrue(hasattr(field, '_storage_callable'))
        self.assertIs(field._storage_callable, GetStorage)

    def test_callable_function_deconstruct_returns_callable_and_attr_matches(self):

        def get_storage():
            return FileSystemStorage()
        field = FileField(storage=get_storage)
        name, path, args, kwargs = field.deconstruct()
        self.assertIn('storage', kwargs)
        self.assertIs(kwargs['storage'], get_storage)
        self.assertTrue(hasattr(field, '_storage_callable'))
        self.assertIs(field._storage_callable, get_storage)

    def test_callable_class_deconstruct_returns_callable_and_attr_matches(self):

        class GetStorage(FileSystemStorage):
            pass
        field = FileField(storage=GetStorage)
        name, path, args, kwargs = field.deconstruct()
        self.assertIn('storage', kwargs)
        self.assertIs(kwargs['storage'], GetStorage)
        self.assertTrue(hasattr(field, '_storage_callable'))
        self.assertIs(field._storage_callable, GetStorage)

    def test_model_field_callable_storage_sets__storage_callable(self):
        field = Storage._meta.get_field('storage_callable')
        self.assertTrue(hasattr(field, '_storage_callable'))
        self.assertIs(field._storage_callable, callable_storage)

    def test_model_field_callable_storage_deconstruct_preserves_callable(self):
        field = Storage._meta.get_field('storage_callable')
        name, path, args, kwargs = field.deconstruct()
        self.assertIn('storage', kwargs)
        self.assertIs(kwargs['storage'], callable_storage)
        self.assertTrue(hasattr(field, '_storage_callable'))
        self.assertIs(field._storage_callable, callable_storage)

    def test_callable_class_storage_attr_and_deconstruct_persist(self):

        class GetStorage(FileSystemStorage):
            pass
        field = FileField(storage=GetStorage)
        self.assertTrue(hasattr(field, '_storage_callable'))
        self.assertIs(field._storage_callable, GetStorage)
        _, _, _, kwargs = field.deconstruct()
        self.assertIn('storage', kwargs)
        self.assertIs(kwargs['storage'], GetStorage)

    def test_deconstruct_does_not_remove__storage_callable_attribute(self):

        def get_storage():
            return FileSystemStorage()
        field = FileField(storage=get_storage)
        _ = field.deconstruct()
        self.assertTrue(hasattr(field, '_storage_callable'))
        self.assertIs(field._storage_callable, get_storage)

import tempfile
import shutil
from django.test import SimpleTestCase
from django.core.files.storage import default_storage, FileSystemStorage
from django.db.models import FileField
import tempfile
import shutil
from django.test import SimpleTestCase
from django.core.files.storage import default_storage, FileSystemStorage
from django.db.models import FileField

class FileFieldDeconstructTests(SimpleTestCase):

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()

    def test_deconstruct_omits_storage_when_callable_returns_default_storage(self):

        def return_default():
            return default_storage
        f = FileField(storage=return_default)
        _, _, _, kwargs = f.deconstruct()
        self.assertNotIn('storage', kwargs)

    def test_deconstruct_omits_storage_when_lambda_returns_default_storage(self):
        f = FileField(storage=lambda: default_storage)
        _, _, _, kwargs = f.deconstruct()
        self.assertNotIn('storage', kwargs)

    def test_deconstruct_callable_that_returns_default_storage_not_in_kwargs_even_if_callable_is_distinct(self):

        def returns_default_named():
            return default_storage
        f = FileField(storage=returns_default_named)
        _, _, _, kwargs = f.deconstruct()
        self.assertNotIn('storage', kwargs)

from functools import partial
from functools import partial
from django.test import SimpleTestCase
from django.db.models import FileField
from django.core.files.storage import default_storage

class DeconstructCallableReturningDefaultStorageTests(SimpleTestCase):

    def test_function_returning_default_storage_is_omitted(self):

        def get_default():
            return default_storage
        _, _, _, kwargs = FileField(storage=get_default).deconstruct()
        self.assertNotIn('storage', kwargs)

    def test_lambda_returning_default_storage_is_omitted(self):
        getter = lambda: default_storage
        _, _, _, kwargs = FileField(storage=getter).deconstruct()
        self.assertNotIn('storage', kwargs)

    def test_callable_instance_returning_default_storage_is_omitted(self):

        class ReturnDefault:

            def __call__(self):
                return default_storage
        inst = ReturnDefault()
        _, _, _, kwargs = FileField(storage=inst).deconstruct()
        self.assertNotIn('storage', kwargs)

    def test_partial_of_function_returning_default_storage_is_omitted(self):

        def get_default():
            return default_storage
        p = partial(get_default)
        _, _, _, kwargs = FileField(storage=p).deconstruct()
        self.assertNotIn('storage', kwargs)

    def test_bound_method_returning_default_storage_is_omitted(self):

        class C:

            def method(self):
                return default_storage
        c = C()
        _, _, _, kwargs = FileField(storage=c.method).deconstruct()
        self.assertNotIn('storage', kwargs)

    def test_closure_returning_default_storage_is_omitted(self):

        def outer():

            def inner():
                return default_storage
            return inner
        getter = outer()
        _, _, _, kwargs = FileField(storage=getter).deconstruct()
        self.assertNotIn('storage', kwargs)

    def test_nested_callable_returning_default_storage_is_omitted(self):

        def outer_callable():
            return default_storage

        def wrapper():
            return outer_callable()
        _, _, _, kwargs = FileField(storage=wrapper).deconstruct()
        self.assertNotIn('storage', kwargs)

    def test_generator_based_callable_wrapper_returning_default_storage_is_omitted(self):

        class GenWrapper:

            def __call__(self):

                def gen():
                    yield 1
                list(gen())
                return default_storage
        _, _, _, kwargs = FileField(storage=GenWrapper()).deconstruct()
        self.assertNotIn('storage', kwargs)

    def test_partial_wrapping_callable_instance_returning_default_storage_is_omitted(self):

        class ReturnDefault:

            def __call__(self):
                return default_storage
        inst = ReturnDefault()
        p = partial(inst)
        _, _, _, kwargs = FileField(storage=p).deconstruct()
        self.assertNotIn('storage', kwargs)

import shutil
import tempfile
from functools import partial
from django.core.files.storage import FileSystemStorage
from django.db.models.fields.files import FileField
from django.test import SimpleTestCase
import shutil
import tempfile
from functools import partial
from django.core.files.storage import FileSystemStorage
from django.db.models.fields.files import FileField
from django.test import SimpleTestCase

class FileFieldStorageCallableRetentionTests(SimpleTestCase):

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp(suffix='filefield_storage_callable_test')

    def test_function_callable_sets__storage_callable(self):

        def get_storage():
            return FileSystemStorage(location=self.temp_dir)
        field = FileField(storage=get_storage)
        self.assertTrue(hasattr(field, '_storage_callable'))
        self.assertIs(field._storage_callable, get_storage)
        self.assertIsInstance(field.storage, FileSystemStorage)

    def test_class_callable_sets__storage_callable(self):

        class GetStorage(FileSystemStorage):
            pass
        field = FileField(storage=GetStorage)
        self.assertTrue(hasattr(field, '_storage_callable'))
        self.assertIs(field._storage_callable, GetStorage)
        self.assertIsInstance(field.storage, FileSystemStorage)

    def test_partial_callable_sets__storage_callable(self):

        def factory(location):
            return FileSystemStorage(location=location)
        part = partial(factory, self.temp_dir)
        field = FileField(storage=part)
        self.assertTrue(hasattr(field, '_storage_callable'))
        self.assertIs(field._storage_callable, part)
        self.assertIsInstance(field.storage, FileSystemStorage)

    def test_lambda_callable_sets__storage_callable(self):
        lam = lambda: FileSystemStorage(location=self.temp_dir)
        field = FileField(storage=lam)
        self.assertTrue(hasattr(field, '_storage_callable'))
        self.assertIs(field._storage_callable, lam)
        self.assertIsInstance(field.storage, FileSystemStorage)

    def test_attribute_persists_after_deconstruct(self):

        def get_storage():
            return FileSystemStorage(location=self.temp_dir)
        field = FileField(storage=get_storage)
        field.deconstruct()
        self.assertTrue(hasattr(field, '_storage_callable'))
        self.assertIs(field._storage_callable, get_storage)

    def test_partial_and_lambda_callable_deconstruct_and_attribute(self):

        def factory(location):
            return FileSystemStorage(location=location)
        part = partial(factory, self.temp_dir)
        lam = lambda: FileSystemStorage(location=self.temp_dir)
        part_field = FileField(storage=part)
        lam_field = FileField(storage=lam)
        self.assertTrue(hasattr(part_field, '_storage_callable'))
        self.assertIs(part_field._storage_callable, part)
        self.assertTrue(hasattr(lam_field, '_storage_callable'))
        self.assertIs(lam_field._storage_callable, lam)
        _, _, _, kwargs_part = part_field.deconstruct()
        _, _, _, kwargs_lam = lam_field.deconstruct()
        self.assertIs(kwargs_part.get('storage'), part)
        self.assertIs(kwargs_lam.get('storage'), lam)

import tempfile
import shutil
import unittest
from django.core.files.storage import FileSystemStorage, default_storage
from django.db.models.fields.files import FileField

class FileFieldCallableDeconstructionTests(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()

    def test_deconstruct_omits_storage_when_callable_returns_default_storage(self):
        """
        When a callable is provided which, when called, returns the default_storage
        instance, deconstruct() should still omit the storage kwarg (gold patch
        preserves the behavior of not emitting default_storage in deconstruction).

        The candidate model patch includes the original callable in kwargs
        (because it checks the original passed value rather than the resolved
        storage), which is incorrect per the intended behavior fixed by the
        gold patch. This test will catch that regression.
        """

        def return_default_storage():
            return default_storage
        field = FileField(storage=return_default_storage)
        self.assertIs(field.storage, default_storage)
        _, _, _, kwargs = field.deconstruct()
        self.assertNotIn('storage', kwargs)

    def test_sets__storage_callable_attribute_for_callable(self):
        """
        The gold patch records the original callable on the FileField instance
        as _storage_callable. That attribute should exist and reference the
        original callable. The candidate model patch removed/renamed that,
        so this test will fail under the candidate patch.
        """

        def get_storage():
            return FileSystemStorage(location=self.temp_dir)
        field = FileField(storage=get_storage)
        self.assertTrue(hasattr(field, '_storage_callable'))
        self.assertIs(field._storage_callable, get_storage)

    def test_callable_attribute_exists_but_deconstruct_omits_default(self):
        """
        Mixed assertion: for a callable that returns default_storage, the field
        should still hang on to the original callable as _storage_callable,
        but deconstruct() should omit the 'storage' kwarg (since it resolves to
        default_storage).

        This tests both the presence of the attribute (gold patch) and the
        deconstruction behavior (gold patch). The candidate patch either
        omits the attribute or includes the callable in deconstruct(),
        causing a failure.
        """

        def return_default_storage():
            return default_storage
        field = FileField(storage=return_default_storage)
        self.assertTrue(hasattr(field, '_storage_callable'))
        self.assertIs(field._storage_callable, return_default_storage)
        _, _, _, kwargs = field.deconstruct()
        self.assertNotIn('storage', kwargs)
if __name__ == '__main__':
    unittest.main()

import types
from django.test import SimpleTestCase
from django.core.files.storage import FileSystemStorage, Storage
from django.db.models import FileField

def make_storage_instance():
    """A simple factory function that returns a FileSystemStorage instance."""
    return FileSystemStorage()
assert issubclass(FileSystemStorage, Storage)

import shutil
import tempfile
from django.test import SimpleTestCase
from django.core.files.storage import FileSystemStorage, default_storage
from django.db.models import FileField

class FileFieldDeconstructTests(SimpleTestCase):

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()

    def test_callable_returning_default_storage_excluded(self):

        def get_default():
            return default_storage
        field = FileField(storage=get_default)
        _, _, _, kwargs = field.deconstruct()
        self.assertNotIn('storage', kwargs)

    def test_lambda_returning_default_storage_excluded(self):
        getter = lambda: default_storage
        field = FileField(storage=getter)
        _, _, _, kwargs = field.deconstruct()
        self.assertNotIn('storage', kwargs)

    def test_callable_returning_default_storage_via_factory_function(self):

        def factory():
            return default_storage
        field = FileField(storage=factory)
        _, _, _, kwargs = field.deconstruct()
        self.assertNotIn('storage', kwargs)

    def test_callable_returning_default_storage_does_not_store_callable(self):

        def unique_getter():
            return default_storage
        field = FileField(storage=unique_getter)
        _, _, _, kwargs = field.deconstruct()
        self.assertNotIn('storage', kwargs)

import functools
from django.test import SimpleTestCase
from django.db.models import FileField
from django.core.files.storage import default_storage
import functools


class FileFieldDeconstructCallableReturnsDefaultStorageTests(SimpleTestCase):
    def test_deconstruct_omits_storage_for_function_returning_default_storage(self):
        def get_default():
            return default_storage
        _, _, _, kwargs = FileField(storage=get_default).deconstruct()
        self.assertNotIn('storage', kwargs)

    def test_deconstruct_omits_storage_for_lambda_returning_default_storage(self):
        get_default = lambda: default_storage
        _, _, _, kwargs = FileField(storage=get_default).deconstruct()
        self.assertNotIn('storage', kwargs)

    def test_deconstruct_omits_storage_for_partial_returning_default_storage(self):
        def get_default():
            return default_storage
        p = functools.partial(get_default)
        _, _, _, kwargs = FileField(storage=p).deconstruct()
        self.assertNotIn('storage', kwargs)

    def test_deconstruct_omits_storage_for_bound_method_returning_default_storage(self):
        class Wrapper:
            def get(self):
                return default_storage
        w = Wrapper()
        _, _, _, kwargs = FileField(storage=w.get).deconstruct()
        self.assertNotIn('storage', kwargs)

    def test_deconstruct_omits_storage_for_staticmethod_returning_default_storage(self):
        class Wrapper:
            @staticmethod
            def get():
                return default_storage
        # Accessing as attribute on class returns function object
        _, _, _, kwargs = FileField(storage=Wrapper.get).deconstruct()
        self.assertNotIn('storage', kwargs)

    def test_deconstruct_omits_storage_for_callable_object_instance(self):
        class CallableObj:
            def __call__(self):
                return default_storage
        obj = CallableObj()
        _, _, _, kwargs = FileField(storage=obj).deconstruct()
        self.assertNotIn('storage', kwargs)

    def test_deconstruct_omits_storage_for_class_with_new_returning_default_storage(self):
        # A class whose __new__ returns default_storage (so calling the class
        # yields default_storage). This exercises callable classes that
        # directly return the default instance.
        class ReturnDefault:
            def __new__(cls):
                return default_storage
        _, _, _, kwargs = FileField(storage=ReturnDefault).deconstruct()
        self.assertNotIn('storage', kwargs)

    def test_deconstruct_omits_storage_for_nested_function_returning_default_storage(self):
        def outer():
            def inner():
                return default_storage
            return inner
        nested = outer()
        _, _, _, kwargs = FileField(storage=nested).deconstruct()
        self.assertNotIn('storage', kwargs)

    def test_deconstruct_omits_storage_for_exec_created_function_returning_default_storage(self):
        # Create a function dynamically via exec that returns default_storage.
        ns = {}
        code = "def dynamic_get():\n    return default_storage"
        exec(code, {'default_storage': default_storage}, ns)
        dynamic_get = ns['dynamic_get']
        _, _, _, kwargs = FileField(storage=dynamic_get).deconstruct()
        self.assertNotIn('storage', kwargs)

    def test_reconstruct_without_storage_uses_default_storage(self):
        # Ensure that when a callable (that returns default_storage) is used,
        # deconstruction omits 'storage' and reconstructing from kwargs uses default_storage.
        def get_default():
            return default_storage
        _, _, _, kwargs = FileField(storage=get_default).deconstruct()
        # storage should be omitted in kwargs; reconstructing from kwargs should give default_storage
        self.assertNotIn('storage', kwargs)
        reconstructed = FileField(**kwargs)
        self.assertIs(reconstructed.storage, default_storage)

import functools
import tempfile
import shutil
from django.db import models
from django.core.files.storage import FileSystemStorage
from django.db.models import FileField
from django.test import SimpleTestCase

class FileFieldStorageCallableAttributeTests(SimpleTestCase):

    def _make_storage_callable(self, location=None):

        def _get_storage():
            return FileSystemStorage(location=location) if location is not None else FileSystemStorage()
        return _get_storage

    def test_function_callable_sets_storage_callable_and_deconstruct(self):
        temp_dir = tempfile.mkdtemp()
        try:
            get_storage = self._make_storage_callable(location=temp_dir)
            field = FileField(storage=get_storage)
            self.assertTrue(hasattr(field, '_storage_callable'))
            self.assertIs(field._storage_callable, get_storage)
            *_, kwargs = field.deconstruct()
            self.assertIn('storage', kwargs)
            self.assertIs(kwargs['storage'], get_storage)
        finally:
            shutil.rmtree(temp_dir)

    def test_class_callable_sets_storage_callable_and_deconstruct(self):
        temp_dir = tempfile.mkdtemp()
        try:

            class GetStorage(FileSystemStorage):
                pass

            def get_storage_class():
                return GetStorage(location=temp_dir)
            field = FileField(storage=get_storage_class)
            self.assertTrue(hasattr(field, '_storage_callable'))
            self.assertIs(field._storage_callable, get_storage_class)
            *_, kwargs = field.deconstruct()
            self.assertIn('storage', kwargs)
            self.assertIs(kwargs['storage'], get_storage_class)
        finally:
            shutil.rmtree(temp_dir)

    def test_callable_object_sets_storage_callable_and_deconstruct(self):
        temp_dir = tempfile.mkdtemp()
        try:

            class CallableObj:

                def __call__(self):
                    return FileSystemStorage(location=temp_dir)
            obj = CallableObj()
            field = FileField(storage=obj)
            self.assertTrue(hasattr(field, '_storage_callable'))
            self.assertIs(field._storage_callable, obj)
            *_, kwargs = field.deconstruct()
            self.assertIn('storage', kwargs)
            self.assertIs(kwargs['storage'], obj)
        finally:
            shutil.rmtree(temp_dir)

    def test_lambda_callable_sets_storage_callable_and_deconstruct(self):
        temp_dir = tempfile.mkdtemp()
        try:
            get_storage = lambda: FileSystemStorage(location=temp_dir)
            field = FileField(storage=get_storage)
            self.assertTrue(hasattr(field, '_storage_callable'))
            self.assertIs(field._storage_callable, get_storage)
            *_, kwargs = field.deconstruct()
            self.assertIn('storage', kwargs)
            self.assertIs(kwargs['storage'], get_storage)
        finally:
            shutil.rmtree(temp_dir)

    def test_partial_callable_sets_storage_callable_and_deconstruct(self):
        temp_dir = tempfile.mkdtemp()
        try:
            get_storage = functools.partial(FileSystemStorage, location=temp_dir)
            field = FileField(storage=get_storage)
            self.assertTrue(hasattr(field, '_storage_callable'))
            self.assertIs(field._storage_callable, get_storage)
            *_, kwargs = field.deconstruct()
            self.assertIn('storage', kwargs)
            self.assertIs(kwargs['storage'], get_storage)
        finally:
            shutil.rmtree(temp_dir)

    def test_model_field_callable_sets_storage_callable_attribute(self):
        temp_dir = tempfile.mkdtemp()
        try:

            def get_storage():
                return FileSystemStorage(location=temp_dir)

            class TestModel(models.Model):
                file = FileField(storage=get_storage)

                class Meta:
                    app_label = 'tests'
            field = TestModel._meta.get_field('file')
            self.assertTrue(hasattr(field, '_storage_callable'))
            self.assertIs(field._storage_callable, get_storage)
            *_, kwargs = field.deconstruct()
            self.assertIn('storage', kwargs)
            self.assertIs(kwargs['storage'], get_storage)
        finally:
            shutil.rmtree(temp_dir)