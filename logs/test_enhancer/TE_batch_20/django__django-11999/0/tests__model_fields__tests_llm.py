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