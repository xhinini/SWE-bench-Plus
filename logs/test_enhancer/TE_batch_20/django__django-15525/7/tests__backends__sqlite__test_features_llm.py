from types import SimpleNamespace
import unittest
from django.core.serializers.base import build_instance
from types import SimpleNamespace
import unittest
from django.core.serializers.base import build_instance

def make_fake_model(*, pk_attname='id', pk_to_python=lambda v: int(v), manager_has_get_by_natural_key=True, manager_result_pk='123', manager_raises_doesnotexist=False, natural_key_func=None):
    """
    Returns (ModelClass, manager_instance) where:
    - ModelClass._meta.pk.attname == pk_attname
    - ModelClass._meta.pk.to_python calls pk_to_python
    - ModelClass._meta.default_manager implements db_manager(...).get_by_natural_key(...)
    - natural_key_func(instance) is used for natural_key (if provided),
      else returns tuple ('nk',)
    """

    class FakePK:

        def __init__(self, attname, to_python_func):
            self.attname = attname
            self._to_python = to_python_func

        def to_python(self, value):
            return self._to_python(value)

    class Manager:

        def __init__(self):
            self.db = None
            self.last_args = None

        def db_manager(self, db):
            self.db = db
            return self
        if manager_has_get_by_natural_key:

            def get_by_natural_key(self, *args):
                self.last_args = args
                if manager_raises_doesnotexist:
                    raise DummyDoesNotExist()
                return SimpleNamespace(pk=manager_result_pk)

    class Meta:
        pass

    def default_natural_key(self):
        if natural_key_func is not None:
            return natural_key_func(self)
        return ('nk',)

    class FakeModel:
        DoesNotExist = DummyDoesNotExist
        _meta = Meta()
        _meta.default_manager = Manager()
        _meta.pk = FakePK(pk_attname, pk_to_python)

        def __init__(self, **kwargs):
            self._state = SimpleNamespace(db=None)
            for k, v in kwargs.items():
                setattr(self, k, v)
        natural_key = default_natural_key
    return (FakeModel, FakeModel._meta.default_manager)
if __name__ == '__main__':
    unittest.main()

from types import SimpleNamespace
from types import SimpleNamespace
import unittest
from django.core.serializers.base import build_instance

def make_model(natural_key_func, pk_value='42', pk_attname='id'):
    """
    Helper to create a minimal Model-like class for testing build_instance.
    The returned tuple is (ModelClass, manager_instance) where manager_instance
    records the last db used when db_manager(db) is called.
    """

    class DummyManager:

        def __init__(self, pk_value):
            self.pk_value = pk_value
            self.last_db = None

        def db_manager(self, db):
            self.last_db = db
            return self

        def get_by_natural_key(self, *args):
            return SimpleNamespace(pk=self.pk_value)

    class Meta:
        pass
    Meta.pk = SimpleNamespace(attname=pk_attname, to_python=lambda x: int(x))
    manager = DummyManager(pk_value)
    Meta.default_manager = manager
    Meta.app_label = 'tests'
    Meta.model_name = 'dummy'

    class Model:
        _meta = Meta
        DoesNotExist = Exception

        def __init__(self, **data):
            self._state = SimpleNamespace(db=None)
            for k, v in data.items():
                setattr(self, k, v)

        def natural_key(self):
            return natural_key_func(self)
    return (Model, manager)
if __name__ == '__main__':
    unittest.main()

from types import SimpleNamespace
import unittest
from django.core.serializers.base import build_instance

def make_fake_model(natural_key_func, pk_value, pk_conv=lambda v: v, remote_field_names=()):
    """
    Build a fake Model class compatible with build_instance.
    natural_key_func: function(self) -> tuple used as natural_key.
    pk_value: value that default_manager.get_by_natural_key should return as .pk
    pk_conv: function applied by _meta.pk.to_python
    remote_field_names: iterable of field names that should be considered relational
    """

    class FakePK:
        attname = 'id'

        def to_python(self, value):
            return pk_conv(value)

    class FakeField:

        def __init__(self, name):
            self.remote_field = object() if name in remote_field_names else None
            self.name = name

    class DefaultManager:

        def db_manager(self, using):
            self._used_db = using
            return self

        def get_by_natural_key(self, *args):
            return SimpleNamespace(pk=pk_value)

    class Meta:
        pk = FakePK()
        default_manager = DefaultManager()
        app_label = 'app'
        model_name = 'model'

        def get_field(self, name):
            return FakeField(name)

    class Model:
        _meta = Meta()
        DoesNotExist = Exception

        def __init__(self, **data):
            for k, v in data.items():
                setattr(self, k, v)
            self._state = SimpleNamespace(db=None)

        def natural_key(self):
            return natural_key_func(self)
    return Model
if __name__ == '__main__':
    unittest.main()

from types import SimpleNamespace
from types import SimpleNamespace as _SimpleNamespace
import unittest
from types import SimpleNamespace
from django.core.serializers.base import build_instance

def make_model(manager, pk_to_python=lambda x: int(x)):
    """
    Build a minimal Model-like class usable by build_instance.
    """

    class Model:
        DoesNotExist = DummyDoesNotExist
    Model._meta = SimpleNamespace(default_manager=manager, pk=SimpleNamespace(attname='id', to_python=pk_to_python))

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)
        self._state = SimpleNamespace(db=None)
    Model.__init__ = __init__
    return Model
if __name__ == '__main__':
    unittest.main()

from types import SimpleNamespace
from types import SimpleNamespace
import unittest
from django.core.serializers.base import build_instance

def make_model(natural_key_func, pk_by_db, pk_attname='id', to_python=lambda x: int(x)):
    """
    Helper to create a fake Model-like class for testing build_instance.

    natural_key_func: function(self) -> tuple used as Model.natural_key
    pk_by_db: dict mapping db alias -> pk to return from get_by_natural_key
    """

    class DefaultManager:

        def __init__(self, pk_by_db):
            self._pk_by_db = pk_by_db

        def get_by_natural_key(self, *args, **kwargs):
            raise NotImplementedError('use db_manager(...).get_by_natural_key')

        def db_manager(self, db):

            def get_by_natural_key_inner(*args):
                if db not in self._pk_by_db:
                    raise Model.DoesNotExist('not found')
                return SimpleNamespace(pk=self._pk_by_db[db])
            return SimpleNamespace(get_by_natural_key=get_by_natural_key_inner)

    class PKDescriptor:

        def __init__(self, attname, to_python):
            self.attname = attname
            self.to_python = staticmethod(to_python)

    class ModelClass:
        DoesNotExist = type('DoesNotExist', (Exception,), {})
        _meta = SimpleNamespace(pk=PKDescriptor(pk_attname, to_python), default_manager=DefaultManager(pk_by_db))

        def __init__(self, **data):
            for k, v in data.items():
                setattr(self, k, v)
            self._state = SimpleNamespace(db=None)

        def natural_key(self):
            return natural_key_func(self)
    return ModelClass
if __name__ == '__main__':
    unittest.main()