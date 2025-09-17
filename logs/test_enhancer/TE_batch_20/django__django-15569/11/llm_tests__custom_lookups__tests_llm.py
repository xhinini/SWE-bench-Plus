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