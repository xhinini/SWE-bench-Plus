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