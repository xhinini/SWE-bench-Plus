from django.contrib.auth.hashers import UNUSABLE_PASSWORD_PREFIX
from django.forms.fields import Field
from django.test import SimpleTestCase, TestCase
from django.contrib.auth.forms import ReadOnlyPasswordHashField, ReadOnlyPasswordHashWidget, UserChangeForm
from django.contrib.auth.models import User
from .test_forms import TestDataMixin
from django.utils.translation import gettext as _
from django.contrib.auth.hashers import UNUSABLE_PASSWORD_PREFIX

class ReadOnlyPasswordHashFieldMethodTests(SimpleTestCase):

    def test_no_bound_data_method_in_class(self):
        self.assertNotIn('bound_data', ReadOnlyPasswordHashField.__dict__)

    def test_no_has_changed_method_in_class(self):
        self.assertNotIn('has_changed', ReadOnlyPasswordHashField.__dict__)

    def test_bound_data_is_inherited_from_field(self):
        self.assertIs(ReadOnlyPasswordHashField.bound_data, Field.bound_data)

    def test_has_changed_is_inherited_from_field(self):
        self.assertIs(ReadOnlyPasswordHashField.has_changed, Field.has_changed)

class ReadOnlyPasswordHashFieldIntegrationTests(TestDataMixin, TestCase):

    def test_userchangeform_does_not_define_clean_password(self):
        self.assertNotIn('clean_password', UserChangeForm.__dict__)

from django.test import SimpleTestCase
from django.forms.fields import Field
from django.contrib.auth.forms import ReadOnlyPasswordHashField, ReadOnlyPasswordHashWidget, UserChangeForm

class ReadOnlyPasswordFieldAndUserChangeFormRegressionTests(SimpleTestCase):

    def test_readonlyfield_has_no_bound_data_method(self):
        self.assertNotIn('bound_data', ReadOnlyPasswordHashField.__dict__)

    def test_readonlyfield_has_no_has_changed_method(self):
        self.assertNotIn('has_changed', ReadOnlyPasswordHashField.__dict__)

    def test_userchangeform_has_no_clean_password_method(self):
        self.assertNotIn('clean_password', UserChangeForm.__dict__)

    def test_userchangeform_instance_has_no_clean_password_method(self):
        form = UserChangeForm()
        self.assertFalse(hasattr(form, 'clean_password'))

    def test_subclass_does_not_inherit_clean_password(self):

        class SubForm(UserChangeForm):
            pass
        self.assertNotIn('clean_password', SubForm.__dict__)
        self.assertFalse(hasattr(SubForm, 'clean_password'))

from django import forms
from django import forms
from django.test import TestCase
from django.contrib.auth.forms import ReadOnlyPasswordHashField, UserChangeForm
from django.contrib.auth.models import User

class ReadOnlyPasswordHashFieldEnabledTests(TestCase):

    def test_bound_data_returns_data_when_enabled(self):
        field = ReadOnlyPasswordHashField()
        field.disabled = False
        data = 'new_value'
        initial = 'initial_value'
        self.assertEqual(field.bound_data(data, initial), data)

    def test_bound_data_returns_none_when_enabled_and_data_none(self):
        field = ReadOnlyPasswordHashField()
        field.disabled = False
        data = None
        initial = 'initial_value'
        self.assertIs(field.bound_data(data, initial), None)

    def test_form_accepts_posted_password_when_field_enabled(self):

        class F(forms.Form):
            password = ReadOnlyPasswordHashField()
        form = F(data={'password': 'posted_pass'}, initial={'password': 'initial_pass'})
        form.fields['password'].disabled = False
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['password'], 'posted_pass')
        self.assertIn('password', form.changed_data)

    def test_form_enabled_with_empty_string_uses_posted_empty_string(self):

        class F(forms.Form):
            password = ReadOnlyPasswordHashField(required=False)
        form = F(data={'password': ''}, initial={'password': 'initial_pass'})
        form.fields['password'].disabled = False
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['password'], '')
        self.assertIn('password', form.changed_data)

    def test_field_has_changed_reflects_data_when_enabled(self):
        field = ReadOnlyPasswordHashField()
        field.disabled = False
        self.assertTrue(field.has_changed('initial', 'posted'))

    def test_form_binding_unicode_values_when_enabled(self):

        class F(forms.Form):
            password = ReadOnlyPasswordHashField(required=False)
        form = F(data={'password': 'β'}, initial={'password': 'α'})
        form.fields['password'].disabled = False
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['password'], 'β')
        self.assertIn('password', form.changed_data)

from django import forms
from django.test import SimpleTestCase
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django import forms
from django.test import SimpleTestCase
from django.contrib.auth.forms import ReadOnlyPasswordHashField

class ReadOnlyPasswordHashFieldExtraTests(SimpleTestCase):

    def test_has_changed_when_not_disabled(self):
        field = ReadOnlyPasswordHashField()
        field.disabled = False
        self.assertTrue(field.has_changed('old_password_hash', 'new_value'))

    def test_bound_data_returns_data_when_not_disabled(self):
        field = ReadOnlyPasswordHashField()
        field.disabled = False
        self.assertEqual(field.bound_data('posted_value', 'initial_value'), 'posted_value')

    def test_has_changed_with_none_initial_and_nonempty_data_when_not_disabled(self):
        field = ReadOnlyPasswordHashField()
        field.disabled = False
        self.assertTrue(field.has_changed(None, 'nonempty'))

    def test_has_changed_with_empty_string_difference(self):
        field = ReadOnlyPasswordHashField()
        field.disabled = False
        self.assertTrue(field.has_changed('', ' '))

    def test_bound_data_with_empty_initial_when_not_disabled(self):
        field = ReadOnlyPasswordHashField()
        field.disabled = False
        self.assertEqual(field.bound_data('posted', ''), 'posted')

    def test_integration_with_form_has_changed_respects_disabled_flag(self):

        class TestForm(forms.Form):
            pwd = ReadOnlyPasswordHashField()
        form = TestForm(data={'pwd': 'new'}, initial={'pwd': 'old'})
        form.fields['pwd'].disabled = False
        self.assertTrue(form.has_changed())
        form2 = TestForm(data={'pwd': 'new'}, initial={'pwd': 'old'})
        form2.fields['pwd'].disabled = True
        self.assertFalse(form2.has_changed())

def test_no_bound_data_method_on_class(self):
    self.assertFalse(hasattr(ReadOnlyPasswordHashField, 'bound_data'))

def test_no_bound_data_method_on_instance(self):
    field = ReadOnlyPasswordHashField()
    self.assertFalse(hasattr(field, 'bound_data'))

def test_no_has_changed_method_on_class(self):
    self.assertFalse(hasattr(ReadOnlyPasswordHashField, 'has_changed'))

def test_no_has_changed_method_on_instance(self):
    field = ReadOnlyPasswordHashField()
    self.assertFalse(hasattr(field, 'has_changed'))

def test_bound_data_not_in_dir(self):
    self.assertNotIn('bound_data', dir(ReadOnlyPasswordHashField))
    field = ReadOnlyPasswordHashField()
    self.assertNotIn('bound_data', dir(field))

def test_has_changed_not_in_dir(self):
    self.assertNotIn('has_changed', dir(ReadOnlyPasswordHashField))
    field = ReadOnlyPasswordHashField()
    self.assertNotIn('has_changed', dir(field))

def test_getattr_returns_default_for_bound_data(self):
    self.assertIs(getattr(ReadOnlyPasswordHashField, 'bound_data', None), None)
    field = ReadOnlyPasswordHashField()
    self.assertIs(getattr(field, 'bound_data', None), None)

def test_getattr_returns_default_for_has_changed(self):
    self.assertIs(getattr(ReadOnlyPasswordHashField, 'has_changed', None), None)
    field = ReadOnlyPasswordHashField()
    self.assertIs(getattr(field, 'has_changed', None), None)

def test_class_getattribute_raises_for_bound_data(self):
    with self.assertRaises(AttributeError):
        ReadOnlyPasswordHashField.__getattribute__(ReadOnlyPasswordHashField, 'bound_data')

def test_class_getattribute_raises_for_has_changed(self):
    with self.assertRaises(AttributeError):
        ReadOnlyPasswordHashField.__getattribute__(ReadOnlyPasswordHashField, 'has_changed')

from django.forms.fields import Field
from django.contrib.auth.forms import ReadOnlyPasswordHashField, UserChangeForm, AdminPasswordChangeForm
from django.contrib.auth.models import User
from django.forms.fields import Field
from django.test import SimpleTestCase, TestCase
from django.contrib.auth.forms import ReadOnlyPasswordHashField, UserChangeForm, AdminPasswordChangeForm
from django.contrib.auth.models import User
from .test_forms import TestDataMixin

class ReadOnlyPasswordHashFieldAPITest(SimpleTestCase):

    def test_bound_data_not_overridden_on_class(self):
        self.assertIs(ReadOnlyPasswordHashField.bound_data, Field.bound_data)

    def test_has_changed_not_overridden_on_class(self):
        self.assertIs(ReadOnlyPasswordHashField.has_changed, Field.has_changed)

    def test_bound_data_not_overridden_on_instance(self):
        field = ReadOnlyPasswordHashField()
        self.assertIs(type(field).bound_data, Field.bound_data)

    def test_has_changed_not_overridden_on_instance(self):
        field = ReadOnlyPasswordHashField()
        self.assertIs(type(field).has_changed, Field.has_changed)

    def test_userchangeform_does_not_define_clean_password_on_class(self):
        self.assertNotIn('clean_password', UserChangeForm.__dict__)

    def test_userchangeform_does_not_define_clean_password_on_instance(self):
        form = UserChangeForm()
        self.assertNotIn('clean_password', form.__class__.__dict__)

from django import forms
from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField, UserChangeForm
from django.contrib.auth.models import User
from django.forms.fields import Field
from django.test import TestCase
from .test_forms import TestDataMixin

class ReadOnlyPasswordHashFieldRegressionTests(TestDataMixin, TestCase):

    def test_bound_data_not_overridden_on_field_class(self):
        self.assertIs(ReadOnlyPasswordHashField.bound_data, Field.bound_data)

from django.test import SimpleTestCase
from django.contrib.auth.forms import ReadOnlyPasswordHashField

class ReadOnlyPasswordHashFieldAPIRegressionTests(SimpleTestCase):

    def test_strict_attribute_check_on_class(self):
        self.assertNotIn('bound_data', ReadOnlyPasswordHashField.__dict__)

from django import forms
from django.test import SimpleTestCase
from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField

class ReadOnlyPasswordHashEnabledTests(SimpleTestCase):

    def test_bound_data_returns_posted_value_when_field_enabled(self):
        field = ReadOnlyPasswordHashField(disabled=False)
        self.assertEqual(field.bound_data('new_value', 'initial_value'), 'new_value')

    def test_has_changed_returns_true_when_field_enabled_and_values_differ(self):
        field = ReadOnlyPasswordHashField(disabled=False)
        self.assertTrue(field.has_changed('initial_value', 'new_value'))

    def test_form_changed_data_includes_field_when_enabled_and_posted_value_differs(self):

        class F(forms.Form):
            password = ReadOnlyPasswordHashField(disabled=False)
        form = F(data={'password': 'new_value'}, initial={'password': 'initial_value'})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.changed_data, ['password'])

    def test_bound_data_with_initial_none_returns_posted_value_when_enabled(self):
        field = ReadOnlyPasswordHashField(disabled=False)
        self.assertEqual(field.bound_data('new_value', None), 'new_value')

    def test_has_changed_true_with_initial_none_and_posted_value_when_enabled(self):
        field = ReadOnlyPasswordHashField(disabled=False)
        self.assertTrue(field.has_changed(None, 'new_value'))

    def test_form_changed_data_includes_field_with_initial_empty_string(self):

        class F(forms.Form):
            password = ReadOnlyPasswordHashField(disabled=False)
        form = F(data={'password': 'new_value'}, initial={'password': ''})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.changed_data, ['password'])

    def test_bound_data_returns_empty_string_when_posted_empty_and_enabled(self):
        field = ReadOnlyPasswordHashField(disabled=False)
        self.assertEqual(field.bound_data('', 'initial_value'), '')
        self.assertTrue(field.has_changed('initial_value', ''))

    def test_form_changed_data_detects_change_when_posted_empty_string(self):

        class F(forms.Form):
            password = ReadOnlyPasswordHashField(disabled=False)
        form = F(data={'password': ''}, initial={'password': 'initial_value'})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['password'], '')
        self.assertEqual(form.changed_data, ['password'])

from django import forms
from django.test import SimpleTestCase
from django.contrib.auth.forms import ReadOnlyPasswordHashField

class ReadOnlyPasswordHashFieldUnitTests(SimpleTestCase):

    def test_class_does_not_override_bound_data(self):
        self.assertIs(ReadOnlyPasswordHashField.bound_data, forms.Field.bound_data)

    def test_class_does_not_override_has_changed(self):
        self.assertIs(ReadOnlyPasswordHashField.has_changed, forms.Field.has_changed)