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