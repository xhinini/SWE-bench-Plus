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

from django.core.serializers.base import build_instance
import unittest
import unittest
from django.core.serializers.base import build_instance

def make_model(natural_key_behavior, pk_converter=lambda v: v, manager_mapping=None, manager_raise_on=None):
    """
    Create a fake Model class compatible with build_instance.
    natural_key_behavior: callable accepting (self) and returning a tuple used as natural key.
    manager_mapping: mapping from natural_key[0] -> pk returned by get_by_natural_key
    """

    class FakeModel:

        class DoesNotExist(Exception):
            pass
        _meta = type('m', (), {})()
        _meta.pk = DummyPK(attname='id', to_python=pk_converter)

        def __init__(self, **data):
            for k, v in data.items():
                setattr(self, k, v)
            self._state = type('s', (), {'db': None})()

        def natural_key(self):
            return natural_key_behavior(self)
    mgr = DummyManager(mapping=manager_mapping or {}, raise_on=manager_raise_on)
    mgr.OwnerModel = FakeModel
    FakeModel._meta.default_manager = mgr
    return FakeModel
if __name__ == '__main__':
    unittest.main()

from types import SimpleNamespace
from django.test import SimpleTestCase
from django.core.serializers.base import build_instance

def make_meta(pk_attname='id', pk_converter=lambda x: x, default_manager=None, remote_fields=None):
    remote_fields = {} if remote_fields is None else remote_fields
    pk = FakePK(attname=pk_attname, to_python=pk_converter)

    def get_field(name):
        return SimpleNamespace(remote_field=True if remote_fields.get(name) else None)
    return SimpleNamespace(pk=pk, default_manager=default_manager, get_field=get_field)

def make_model_class(natural_key_callable):
    """
    Build a lightweight pseudo-Model class compatible with build_instance().
    The class accepts kwargs in its __init__ and stores them as attributes;
    it also creates a _state object to mimic Django model state behavior.
    """

    class Model:
        DoesNotExist = Exception

        def __init__(self, **kwargs):
            for k, v in kwargs.items():
                setattr(self, k, v)
            self._state = SimpleNamespace()

        def natural_key(self):
            return natural_key_callable(self)
    return Model

from unittest import TestCase
from types import SimpleNamespace
from django.core.serializers.base import build_instance

def make_model_class(default_manager, pk=None, natural_key_fn=None):
    """
    Create a lightweight dummy Model-like class for testing build_instance.
    """

    class ModelLike:
        DoesNotExist = DummyDoesNotExist
        _meta = SimpleNamespace(default_manager=default_manager, pk=pk or DummyPK())

        def __init__(self, **data):
            for k, v in data.items():
                setattr(self, k, v)
            self._state = SimpleNamespace(db=None)
        if natural_key_fn is None:

            def natural_key(self):
                raise NotImplementedError('natural_key not provided')
        else:

            def natural_key(self, _fn=natural_key_fn):
                return _fn(self)
    return ModelLike

from types import SimpleNamespace
from django.test import SimpleTestCase
from types import SimpleNamespace
from django.core.serializers.base import build_instance

class BuildInstanceTests(SimpleTestCase):

    def test_sets_state_db_before_natural_key(self):
        recorded = {}

        class DummyPK:
            attname = 'id'

            @staticmethod
            def to_python(x):
                return int(x)

        class DummyModel:
            _meta = SimpleNamespace()
            _meta.pk = DummyPK()

            class DoesNotExist(Exception):
                pass

            def __init__(self, **data):
                self.__dict__.update(data)
                self._state = SimpleNamespace(db=None)

            def natural_key(self):
                recorded['db'] = self._state.db
                return ('nk',)

        class Result:

            def __init__(self, pk):
                self.pk = pk

        class DummyManager:

            def __init__(self, result=None, raise_exc=None):
                self._result = result
                self._raise = raise_exc
                self.last_db = None

            def db_manager(self, db):
                self.last_db = db
                return self

            def get_by_natural_key(self, *args):
                if self._raise:
                    raise self._raise
                return self._result
        result = Result(pk='7')
        mgr = DummyManager(result=result)
        DummyModel._meta.default_manager = mgr
        inst = build_instance(DummyModel, {}, 'other')
        self.assertEqual(recorded.get('db'), 'other')
        self.assertEqual(inst.__dict__['id'], 7)

    def test_handles_does_not_exist_from_manager(self):
        recorded = {}

        class DummyPK:
            attname = 'id'

            @staticmethod
            def to_python(x):
                return int(x)

        class DummyModel:
            _meta = SimpleNamespace()
            _meta.pk = DummyPK()

            class DoesNotExist(Exception):
                pass

            def __init__(self, **data):
                self.__dict__.update(data)
                self._state = SimpleNamespace(db=None)

            def natural_key(self):
                recorded['db'] = self._state.db
                return ('missing-nk',)

        class DummyManager:

            def __init__(self):
                self.last_db = None

            def db_manager(self, db):
                self.last_db = db
                return self

            def get_by_natural_key(self, *args):
                raise DummyModel.DoesNotExist()
        DummyModel._meta.default_manager = DummyManager()
        inst = build_instance(DummyModel, {}, 'other_db')
        self.assertEqual(recorded.get('db'), 'other_db')
        self.assertFalse(hasattr(inst, 'id'))

    def test_natural_key_accesses_related_and_sees_state_db(self):
        seen = {}

        class DummyPK:
            attname = 'id'

            @staticmethod
            def to_python(x):
                return int(x)

        class DummyModel:
            _meta = SimpleNamespace()
            _meta.pk = DummyPK()

            class DoesNotExist(Exception):
                pass

            def __init__(self, **data):
                self.__dict__.update(data)
                self._state = SimpleNamespace(db=None)
                self.related = SimpleNamespace(get_name=lambda: f'db={self._state.db}')

            def natural_key(self):
                seen['val'] = self.related.get_name()
                return (seen['val'],)

        class DummyManager:

            def __init__(self, result):
                self._result = result

            def db_manager(self, db):
                return self

            def get_by_natural_key(self, *args):
                return SimpleNamespace(pk='10')
        DummyModel._meta.default_manager = DummyManager(result=None)
        inst = build_instance(DummyModel, {}, 'custom_db')
        self.assertEqual(seen['val'], 'db=custom_db')
        self.assertEqual(inst.id, 10)

    def test_multiple_build_instance_calls_use_provided_db_each_time(self):
        recorded = []

        class DummyPK:
            attname = 'id'

            @staticmethod
            def to_python(x):
                return int(x)

        class DummyModel:
            _meta = SimpleNamespace()
            _meta.pk = DummyPK()

            class DoesNotExist(Exception):
                pass

            def __init__(self, **data):
                self.__dict__.update(data)
                self._state = SimpleNamespace(db=None)

            def natural_key(self):
                recorded.append(self._state.db)
                return ('nk',)

        class DummyManager:

            def __init__(self, pkval):
                self._pk = pkval

            def db_manager(self, db):
                return self

            def get_by_natural_key(self, *args):
                return SimpleNamespace(pk=str(self._pk))
        DummyModel._meta.default_manager = DummyManager(pkval=77)
        inst1 = build_instance(DummyModel, {}, 'db_one')
        DummyModel._meta.default_manager = DummyManager(pkval=88)
        inst2 = build_instance(DummyModel, {}, 'db_two')
        self.assertEqual(recorded, ['db_one', 'db_two'])
        self.assertEqual(inst1.id, 77)
        self.assertEqual(inst2.id, 88)

import unittest
from types import SimpleNamespace
from django.core.serializers.base import build_instance

def make_model_class(*, has_natural_key=True, natural_key_func=None, default_manager=None, pk_attname='id', pk_to_python=lambda x: x, fields_meta=None):
    """
    Dynamically create a Model-like class appropriate for build_instance tests.
    fields_meta: dict mapping field name -> remote_field flag (True/False)
    """

    class ModelLike:
        DoesNotExist = type('DoesNotExist', (Exception,), {})

        def __init__(self, **data):
            for k, v in data.items():
                setattr(self, k, v)
            self._state = SimpleNamespace(db=None)
        _meta = SimpleNamespace()
    ModelLike._meta.pk = DummyPK(attname=pk_attname, to_python=pk_to_python)
    if default_manager is None:
        default_manager = DummyManager(get_by_natural_key_callable=None)
    ModelLike._meta.default_manager = default_manager
    fields_meta = fields_meta or {}

    def get_field(name):

        class FieldObj:

            def __init__(self, remote):
                self.remote_field = True if remote else None
                self.name = name
                self.attname = name
                self.remote_field = SimpleNamespace(model=None) if remote else None
        return FieldObj(fields_meta.get(name, False))
    ModelLike._meta.get_field = staticmethod(get_field)
    if has_natural_key:
        if natural_key_func is None:

            def natural_key(self):
                return ('nk',)
        else:
            natural_key = natural_key_func
        ModelLike.natural_key = natural_key
    return ModelLike
if __name__ == '__main__':
    unittest.main()

import unittest
from types import SimpleNamespace
from django.core.serializers.base import build_instance

def make_model_class(natural_key_func=None, manager_result_pk=None, manager_raises=False, include_get_by=True):
    """
    Create a fake Model class with a _meta.DEFAULT_MANAGER, _meta.pk, and optional
    natural_key implementation. The manager records db_manager() calls and last args.
    """
    DoesNotExist = type('DoesNotExist', (Exception,), {})

    class Meta:
        pk = SimpleNamespace(attname='id', to_python=lambda v: int(v))

    class FakeModel:
        DoesNotExist = DoesNotExist
        _meta = Meta

        def __init__(self, **kwargs):
            self._state = SimpleNamespace(db=None)
            for k, v in kwargs.items():
                setattr(self, k, v)

        def __repr__(self):
            return f"<FakeModel id={getattr(self, 'id', None)}>"

    class Manager:

        def __init__(self):
            self.last_db_manager_arg = None
            self.last_get_by_args = None
            self.result_pk = manager_result_pk
            self.raises = manager_raises

        def db_manager(self, db):
            self.last_db_manager_arg = db
            return self
        if include_get_by:

            def get_by_natural_key(self, *args):
                self.last_get_by_args = args
                if self.raises:
                    raise DoesNotExist()
                return SimpleNamespace(pk=self.result_pk)
    manager = Manager()
    Meta.default_manager = manager
    if natural_key_func:

        def natural_key(self):
            return natural_key_func(self)
        setattr(FakeModel, 'natural_key', natural_key)
    return (FakeModel, manager)
if __name__ == '__main__':
    unittest.main()

import unittest
from types import SimpleNamespace
from django.core.serializers.base import build_instance

def make_manager(return_pk):

    class DefaultManager:

        def db_manager(self, db):
            return self

        def get_by_natural_key(self, *args):
            o = SimpleNamespace(pk=return_pk)
            return o
    return DefaultManager()
if __name__ == '__main__':
    unittest.main()

from types import SimpleNamespace
import unittest
from types import SimpleNamespace
from django.core.serializers import base

def make_meta(default_manager, pk_attname='id', pk_to_python=lambda x: x):

    class PK:
        attname = pk_attname
        to_python = staticmethod(pk_to_python)
    meta = SimpleNamespace()
    meta.default_manager = default_manager
    meta.pk = PK()
    return meta
if __name__ == '__main__':
    unittest.main()