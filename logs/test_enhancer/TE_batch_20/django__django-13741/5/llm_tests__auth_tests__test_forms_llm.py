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