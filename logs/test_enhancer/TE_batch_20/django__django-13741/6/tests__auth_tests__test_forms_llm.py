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