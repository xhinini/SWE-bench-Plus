from django.test import SimpleTestCase
from django.db import models
from .models import Author
from .tests import Exactly

class UnregisterLookupRegressionTests(SimpleTestCase):

    def _field_cls_and_instance(self):
        field_instance = Author._meta.get_field('age')
        return (field_instance.__class__, field_instance)
new_imports_code: ''

from django.db.models.query_utils import RegisterLookupMixin
from django.test import SimpleTestCase
from django.db.models.query_utils import RegisterLookupMixin
import inspect

class TestUnregisterLookupCache(SimpleTestCase):

    def _cleanup(self, *classes):
        for cls in classes:
            if 'class_lookups' in cls.__dict__:
                del cls.class_lookups
        RegisterLookupMixin._clear_cached_lookups()

from django.test import SimpleTestCase
from django.db import models
from django.test import SimpleTestCase
from django.db import models

class RegisterLookupUnregisterTests(SimpleTestCase):

    def test_unregister_on_textfield_affects_customfield_subclass(self):
        Dummy = self._make_lookup('dummy_text_custom')
        parent = models.TextField
        child = None
        for sc in models.TextField.__subclasses__():
            if sc.__name__ == 'CustomField':
                child = sc
                break
        if child is None:
            self.skipTest('CustomField subclass of TextField not present.')
        parent.get_lookups.cache_clear()
        child.get_lookups.cache_clear()
        parent.register_lookup(Dummy)
        _ = child.get_lookups()
        parent._unregister_lookup(Dummy)
        self.assertNotIn('dummy_text_custom', child.get_lookups())

from django.test import SimpleTestCase
from django.db import models

class UnregisterLookupCacheTests(SimpleTestCase):

    def tearDown(self):
        for cls in (models.Field, models.CharField, models.DateField, models.IntegerField):
            try:
                for name in ('dummylu', 'altname', 'otherlu', 'secondlu', 'datedlu'):
                    if hasattr(cls, 'class_lookups') and name in cls.class_lookups:
                        cls._unregister_lookup(cls.class_lookups[name], name)
            except Exception:
                pass
            if hasattr(cls, 'get_lookups'):
                try:
                    cls.get_lookups.cache_clear()
                except Exception:
                    pass