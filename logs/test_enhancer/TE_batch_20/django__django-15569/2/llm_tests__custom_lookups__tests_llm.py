from django.test import SimpleTestCase
from django.db import models
from .models import Author
from .tests import Exactly

class UnregisterLookupRegressionTests(SimpleTestCase):

    def _field_cls_and_instance(self):
        field_instance = Author._meta.get_field('age')
        return (field_instance.__class__, field_instance)
new_imports_code: ''