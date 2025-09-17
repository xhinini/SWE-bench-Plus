from django.test import TestCase
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models.with_many_to_many import CustomUserWithM2M, Organization
from .models.custom_user import ExtensionUser

class UserCreationFormHiddenSaveM2MTests(TestCase):

    def test_hidden_save_m2m_user_model_does_not_raise_on_save(self):
        HiddenForm = self._make_hidden_save_m2m_form(User)
        data = {'username': 'hidden_user_1', 'password1': 'strong-password-1', 'password2': 'strong-password-1'}
        form = HiddenForm(data)
        self.assertTrue(form.is_valid())
        user = form.save()
        self.assertIsInstance(user, User)
        self.assertTrue(User.objects.filter(username='hidden_user_1').exists())

    def test_hidden_save_m2m_extension_user_model_does_not_raise_on_save(self):
        HiddenForm = self._make_hidden_save_m2m_form(ExtensionUser, extra_fields=('date_of_birth',))
        data = {'username': 'hidden_user_2', 'password1': 'strong-password-2', 'password2': 'strong-password-2', 'date_of_birth': '1990-01-01'}
        form = HiddenForm(data)
        self.assertTrue(form.is_valid())
        user = form.save()
        self.assertEqual(user.username, 'hidden_user_2')
        self.assertTrue(ExtensionUser.objects.filter(username='hidden_user_2').exists())

    def test_hidden_save_m2m_after_commit_false_then_commit_true_does_not_raise(self):
        HiddenForm = self._make_hidden_save_m2m_form(User)
        data = {'username': 'hidden_user_4', 'password1': 'strong-password-4', 'password2': 'strong-password-4'}
        form = HiddenForm(data)
        self.assertTrue(form.is_valid())
        user = form.save(commit=False)
        self.assertIsInstance(user, User)
        user2 = form.save()
        self.assertEqual(user.pk, user2.pk)
        self.assertTrue(User.objects.filter(username='hidden_user_4').exists())

    def test_hidden_save_m2m_multiple_saves_does_not_raise(self):
        HiddenForm = self._make_hidden_save_m2m_form(User)
        data = {'username': 'hidden_user_5', 'password1': 'strong-password-5', 'password2': 'strong-password-5'}
        form = HiddenForm(data)
        self.assertTrue(form.is_valid())
        u1 = form.save()
        u2 = form.save()
        self.assertEqual(u1.pk, u2.pk)
        self.assertTrue(User.objects.filter(username='hidden_user_5').exists())

    def test_hidden_save_m2m_with_unicode_username_does_not_raise(self):
        HiddenForm = self._make_hidden_save_m2m_form(User)
        data = {'username': 'ユーザー_hidden_6', 'password1': 'strong-password-6', 'password2': 'strong-password-6'}
        form = HiddenForm(data)
        self.assertTrue(form.is_valid())
        user = form.save()
        self.assertEqual(user.username, 'ユーザー_hidden_6')
        self.assertTrue(User.objects.filter(username='ユーザー_hidden_6').exists())

    def test_hidden_save_m2m_custom_meta_fields_does_not_raise(self):
        HiddenForm = self._make_hidden_save_m2m_form(ExtensionUser, extra_fields=('date_of_birth', 'first_name'))
        data = {'username': 'hidden_user_8', 'password1': 'strong-password-8', 'password2': 'strong-password-8', 'date_of_birth': '2000-01-02', 'first_name': 'Hidden'}
        form = HiddenForm(data)
        self.assertTrue(form.is_valid())
        user = form.save()
        self.assertEqual(user.first_name, 'Hidden')
        self.assertTrue(ExtensionUser.objects.filter(username='hidden_user_8').exists())

    def test_hidden_save_m2m_form_is_valid_and_returns_user_instance(self):
        HiddenForm = self._make_hidden_save_m2m_form(User)
        data = {'username': 'hidden_user_9', 'password1': 'strong-password-9', 'password2': 'strong-password-9'}
        form = HiddenForm(data)
        self.assertTrue(form.is_valid())
        user = form.save()
        self.assertIsInstance(user, User)