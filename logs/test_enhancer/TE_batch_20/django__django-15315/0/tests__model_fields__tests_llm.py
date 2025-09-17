import copy
from django.test import SimpleTestCase
from django import forms
from django.core.exceptions import ValidationError
from django.db import models
import copy

class FieldHashRegressionTests(SimpleTestCase):

    def test_dict_key_survives_model_attach_charfield(self):
        f = models.CharField(max_length=10)
        d = {f: 'char'}

        class MyModel(models.Model):
            name = f
        self.assertEqual(d[f], 'char')