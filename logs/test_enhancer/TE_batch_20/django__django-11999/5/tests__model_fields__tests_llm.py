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

from django.db import models
from django.test import SimpleTestCase

class ContributeToClassDisplayTests(SimpleTestCase):

    def test_metaclass_provided_attribute_preserved(self):
        MetaBase = type(models.Model)

        class CustomMeta(MetaBase):

            def get_x_display(cls):
                return 'metaclass'

        class Base(models.Model, metaclass=CustomMeta):

            class Meta:
                app_label = 'tests'

        class Sub(Base):

            class Meta:
                app_label = 'tests'
            x = models.IntegerField(choices=[(1, 'one')])
        self.assertTrue(callable(getattr(type(Sub), 'get_x_display')))
        self.assertEqual(Sub.get_x_display(), 'metaclass')

    def test_existing_staticmethod_preserved(self):

        class Foo(models.Model):

            class Meta:
                app_label = 'tests'

            @staticmethod
            def get_x_display():
                return 'static'
            x = models.IntegerField(choices=[(1, 'one')])
        f = Foo()
        self.assertEqual(Foo.get_x_display(), 'static')
        self.assertEqual(f.get_x_display(), 'static')