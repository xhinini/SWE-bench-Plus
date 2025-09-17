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