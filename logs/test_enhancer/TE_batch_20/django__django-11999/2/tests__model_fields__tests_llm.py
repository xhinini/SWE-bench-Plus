from django import forms
from django.test import SimpleTestCase
from django.db import models

class DisplayOverrideRegressionTests(SimpleTestCase):

    def test_existing_attribute_none_is_preserved(self):

        class M(models.Model):
            c = models.IntegerField(choices=[(1, 'One')])
            get_c_display = None
        m = M(c=1)
        self.assertIsNone(M.get_c_display)
        with self.assertRaises(TypeError):
            m.get_c_display()

from django.db import models
from django.test import SimpleTestCase
from django import forms
from django.test import SimpleTestCase
from django.db import models

class ContributeToClassDisplayTests(SimpleTestCase):

    def test_inherited_method_not_overridden(self):

        class Parent(models.Model):

            def get_shared_display(self):
                return 'from_parent'

        class Child(Parent):
            shared = models.IntegerField(choices=[(1, 'one')])
        c = Child(shared=1)
        self.assertEqual(c.get_shared_display(), 'from_parent')