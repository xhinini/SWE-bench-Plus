import inspect
import functools
from django.test import SimpleTestCase
from django.db import models as django_models
from django.db.models import manager as manager_mod
from .models import Article

class ManagerWrapsTests(SimpleTestCase):

    def test_module_has_wraps(self):
        self.assertTrue(hasattr(manager_mod, 'wraps'))
        self.assertIs(manager_mod.wraps, functools.wraps)

import inspect
from django.db.models.manager import BaseManager
from django.test import SimpleTestCase
import inspect
from django.db.models.manager import BaseManager

class FromQuerySetMetadataTests(SimpleTestCase):

    def setUp(self):

        class DummyQuerySet:

            def __init__(self, model=None, using=None, hints=None):
                self._init_args = (model, using, hints)

            def custom(self, a, b=2):
                """custom docstring"""
                return a + b

            def varargs(self, *args, **kwargs):
                """varargs doc"""
                return (args, kwargs)

            def _private(self):
                """should be skipped because of leading underscore"""
                return 'private'

            def _special(self, x):
                """should be copied because queryset_only is explicitly False"""
                return x * 2

            def hidden(self):
                """should be skipped because queryset_only is True"""
                return 'hidden'
        DummyQuerySet._special.queryset_only = False
        DummyQuerySet.hidden.queryset_only = True
        self.DummyQuerySet = DummyQuerySet
        ManagerFromDummy = BaseManager.from_queryset(self.DummyQuerySet, class_name='MFD')
        self.manager = ManagerFromDummy()