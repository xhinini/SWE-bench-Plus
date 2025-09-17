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

from django.utils.functional import lazy
from django import forms
from django.test import SimpleTestCase
from django.db import models
from django.utils.functional import lazy

class GetFieldDisplayOverrideRegressionTests(SimpleTestCase):

    def test_existing_attribute_none_not_overridden(self):

        class Base(models.Model):
            get_z_display = None

        class Sub(Base):
            z = models.IntegerField(choices=[(1, 'one')])
        self.assertIsNone(getattr(Sub, 'get_z_display'))

from django.test import SimpleTestCase
from django.db import models

class ContributeToClassDisplayMethodTests(SimpleTestCase):

    def test_existing_descriptor_not_overwritten(self):

        class Descriptor:

            def __get__(self, instance, owner):
                return 'descriptor'

        class M(models.Model):
            get_foo_display = Descriptor()
            foo = models.IntegerField(choices=[(1, 'one')])
        self.assertEqual(M().get_foo_display, 'descriptor')

from django.test import SimpleTestCase
from django.db import models

class ContributeToClassDisplayTests(SimpleTestCase):

    def test_subclass_override_preserved(self):

        class Parent(models.Model):
            pass

        class Child(Parent):

            def get_t_display(self):
                return 'child-method'
            t = models.IntegerField(choices=[(1, 'One')])
        inst = Child(t=1)
        self.assertEqual(inst.get_t_display(), 'child-method')

    def test_classmethod_get_FIELD_display_not_overwritten(self):

        class M(models.Model):

            @classmethod
            def get_u_display(cls):
                return 'classy'
            u = models.IntegerField(choices=[(1, 'One')])
        inst = M(u=1)
        self.assertEqual(inst.get_u_display(), 'classy')

from django import forms
from django.test import SimpleTestCase
from django.db import models

class ContributeToClassDisplayMethodTests(SimpleTestCase):

    def test_field_with_no_choices_does_not_add_display(self):

        class M(models.Model):
            x = models.IntegerField()
        self.assertFalse(hasattr(M, 'get_x_display'))

    def test_subclass_overrides_parent_method_and_is_preserved(self):

        class Base(models.Model):

            def get_a_display(self):
                return 'base_value'

        class Sub(Base):
            a = models.IntegerField(choices=[(1, 'one')])

            def get_a_display(self):
                return 'sub_value'
        inst = Sub(a=1)
        self.assertEqual(inst.get_a_display(), 'sub_value')

from django import forms
from django.db import models
from django.test import SimpleTestCase

class GetFieldDisplayPreservationTests(SimpleTestCase):

    def test_existing_callable_attribute_of_various_kinds_preserved(self):

        def external_func(self):
            return 'external'

        class M(models.Model):
            get_g_display = external_func
            g = models.IntegerField(choices=[(1, 'one')])
        inst = M(g=1)
        self.assertEqual(inst.get_g_display(), 'external')

from django import forms
from django.db import models
from django.test import SimpleTestCase
from django import forms
from django.db import models
from django.test import SimpleTestCase

class PreserveDisplayMethodTests(SimpleTestCase):

    def test_preserve_inherited_display_attribute_none(self):

        class Base(models.Model):
            get_q_display = None

        class Child(Base):
            q = models.IntegerField(choices=[(1, 'one')])
        self.assertTrue(hasattr(Child, 'get_q_display'))
        self.assertIs(Child.get_q_display, None)

from django import forms
from django.core.exceptions import ValidationError
from django.db import models
from django.test import SimpleTestCase
from django.utils.functional import lazy
import types
from django import forms
from django.core.exceptions import ValidationError
from django.db import models
from django.test import SimpleTestCase
from django.utils.functional import lazy

def make_fake_model_class(name, base=object, extra_attrs=None):
    """
    Create a simple class with a per-class _meta and a _get_FIELD_display
    implementation compatible with Field.partialmethod binding used in
    django.db.models.fields.Field.contribute_to_class.
    """
    extra_attrs = dict(extra_attrs or {})

    def _get_FIELD_display(self, field):
        try:
            val = getattr(self, field.attname)
        except AttributeError:
            val = None
        if field.choices is None:
            return val
        for choice, disp in field.choices:
            if isinstance(disp, (list, tuple)):
                for k, v in disp:
                    if k == val:
                        return v
            elif choice == val:
                return disp
        return val
    attrs = {'_meta': FakeMeta(name), '_get_FIELD_display': _get_FIELD_display, '__module__': __name__}
    attrs.update(extra_attrs)
    return types.new_class(name, (base,), {}, lambda ns: ns.update(attrs))

from django.db import models
from django.test import SimpleTestCase
from django.db import models

class ContributeToClassDisplayMethodTests(SimpleTestCase):

    def test_grandparent_method_not_overwritten(self):

        class GrandParent(models.Model):

            def get_gpfield_display(self):
                return 'grandparent'

        class Parent(GrandParent):
            pass

        class Child(Parent):
            gpfield = models.IntegerField(choices=[(1, 'One')])
        inst = Child(gpfield=1)
        self.assertEqual(inst.get_gpfield_display(), 'grandparent')

from django.test import SimpleTestCase
from django.db import models
from django.test import SimpleTestCase
from django.db import models

class ContributeToClassDisplayMethodTests(SimpleTestCase):

    def test_existing_attribute_none_not_overwritten(self):

        class M(models.Model):
            get_foo_display = None
            foo = models.IntegerField(choices=[(1, 'one')])
        self.assertIsNone(getattr(M, 'get_foo_display'))