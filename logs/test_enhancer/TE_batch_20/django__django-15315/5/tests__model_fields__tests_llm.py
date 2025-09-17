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

import copy as _copy
from django.test import SimpleTestCase
from django.db import models

class FieldHashTests(SimpleTestCase):

    def test_set_membership_after_assigning_field_to_model(self):
        f = models.IntegerField()
        s = {f}

        class MyModel(models.Model):
            rank = f
        self.assertIn(f, s)
        self.assertEqual(next(iter(s)).__hash__(), hash(f))

    def test_dict_key_after_manual_model_assignment(self):
        f = models.IntegerField()
        d = {f: 'ok'}

        class M(models.Model):
            pass
        f.model = M
        self.assertEqual(d[f], 'ok')

import copy
import copy
from django.db import models
from django.test import SimpleTestCase

class HashStabilityTests(SimpleTestCase):

    def test_field_dict_key_after_model_assignment_and_removal(self):
        f = models.Field()
        d = {f: 'x'}

        class M(models.Model):
            pass
        f.model = M
        f.__dict__.pop('model', None)
        self.assertEqual(d[f], 'x')