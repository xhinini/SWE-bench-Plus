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

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.test import TestCase
from .models.with_many_to_many import CustomUserWithM2M, Organization

class UserCreationSaveM2MRegressionTests(TestCase):

    def test_save_does_not_raise_if_save_m2m_is_hidden_on_instance(self):

        class NoSaveM2MForm(UserCreationForm):

            def __getattribute__(self, name):
                if name == 'save_m2m':
                    raise AttributeError
                return super().__getattribute__(name)
        data = {'username': 'hiddenm2m', 'password1': 'hiddenpass', 'password2': 'hiddenpass'}
        form = NoSaveM2MForm(data)
        self.assertTrue(form.is_valid())
        user = form.save(commit=True)
        self.assertIsNotNone(user.pk)
        self.assertTrue(user.check_password('hiddenpass'))

    def test_saving_with_hidden_save_m2m_on_form_with_m2m_fields_does_not_raise(self):

        class HiddenM2MForm(UserCreationForm):

            class Meta(UserCreationForm.Meta):
                model = CustomUserWithM2M
                fields = UserCreationForm.Meta.fields + ('orgs',)

            def __getattribute__(self, name):
                if name == 'save_m2m':
                    raise AttributeError
                return super().__getattribute__(name)
        org = Organization.objects.create(name='org3')
        data = {'username': 'hiddenm2m_user', 'password1': 'pass12345', 'password2': 'pass12345', 'orgs': [str(org.pk)]}
        form = HiddenM2MForm(data)
        self.assertTrue(form.is_valid())
        user = form.save(commit=True)
        self.assertIsNotNone(user.pk)

    def test_password_is_set_correctly_when_save_m2m_hidden(self):

        class NoSaveM2MForm(UserCreationForm):

            def __getattribute__(self, name):
                if name == 'save_m2m':
                    raise AttributeError
                return super().__getattribute__(name)
        data = {'username': 'hidden_pw_user', 'password1': 'pw_hidden', 'password2': 'pw_hidden'}
        form = NoSaveM2MForm(data)
        self.assertTrue(form.is_valid())
        user = form.save(commit=True)
        self.assertTrue(user.check_password('pw_hidden'))

from django.test import TestCase
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models.with_many_to_many import CustomUserWithM2M, Organization
User = get_user_model()

class UserCreationSaveM2MRegressionTests(TestCase):

    def setUp(self):
        self.org = Organization.objects.create(name='Org for M2M tests')

# No additional imports required beyond those used in the project test suite; the test file
# imports models from the local tests package (auth_tests) which are reused here.
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import translation

from .models.custom_user import CustomUser, ExtensionUser
from .models.with_many_to_many import CustomUserWithM2M, Organization

class HiddenSaveM2MTests(TestCase):
    def test_hidden_save_m2m_basic_create_user(self):
        class BrokenForm(UserCreationForm):
            def __getattribute__(self, name):
                # Hide the save_m2m attribute from hasattr() by raising AttributeError
                if name == "save_m2m":
                    raise AttributeError
                return super().__getattribute__(name)

        data = {"username": "hidden_save_1", "password1": "test123", "password2": "test123"}
        form = BrokenForm(data)
        self.assertTrue(form.is_valid())
        user = form.save(commit=True)
        # User should be saved to the DB without error
        self.assertEqual(User.objects.get(username="hidden_save_1"), user)

    def test_hidden_save_m2m_sets_password(self):
        class BrokenForm(UserCreationForm):
            def __getattribute__(self, name):
                if name == "save_m2m":
                    raise AttributeError
                return super().__getattribute__(name)

        data = {"username": "hidden_save_2", "password1": "s3cr3t", "password2": "s3cr3t"}
        form = BrokenForm(data)
        self.assertTrue(form.is_valid())
        user = form.save(commit=True)
        # Password should be set correctly
        self.assertTrue(user.check_password("s3cr3t"))

    def test_hidden_save_m2m_unicode_username(self):
        class BrokenForm(UserCreationForm):
            def __getattribute__(self, name):
                if name == "save_m2m":
                    raise AttributeError
                return super().__getattribute__(name)

        username = "宝"
        data = {"username": username, "password1": "test123", "password2": "test123"}
        form = BrokenForm(data)
        self.assertTrue(form.is_valid())
        user = form.save(commit=True)
        self.assertEqual(user.username, username)

    def test_hidden_save_m2m_normalizes_username(self):
        class BrokenForm(UserCreationForm):
            def __getattribute__(self, name):
                if name == "save_m2m":
                    raise AttributeError
                return super().__getattribute__(name)

        ohm_username = "testΩ"  # U+2126 OHM SIGN
        data = {"username": ohm_username, "password1": "pwd2", "password2": "pwd2"}
        form = BrokenForm(data)
        self.assertTrue(form.is_valid())
        user = form.save(commit=True)
        # Normalization should still occur on save
        self.assertEqual(user.username, "testΩ")  # U+03A9 GREEK CAPITAL LETTER OMEGA

    def test_hidden_save_m2m_with_extension_user_model(self):
        class BrokenForm(UserCreationForm):
            class Meta(UserCreationForm.Meta):
                model = ExtensionUser
                fields = UserCreationForm.Meta.fields + ("date_of_birth",)

            def __getattribute__(self, name):
                if name == "save_m2m":
                    raise AttributeError
                return super().__getattribute__(name)

        data = {
            "username": "hidden_save_5",
            "password1": "test123",
            "password2": "test123",
            "date_of_birth": "1990-01-01",
        }
        form = BrokenForm(data)
        self.assertTrue(form.is_valid())
        user = form.save(commit=True)
        self.assertEqual(user.username, "hidden_save_5")
        # The extension field should be present on the instance (ModelForm handled it)
        self.assertEqual(getattr(user, "date_of_birth"), form.cleaned_data["date_of_birth"])

    def test_hidden_save_m2m_with_custom_user_model(self):
        class BrokenForm(UserCreationForm):
            class Meta(UserCreationForm.Meta):
                model = CustomUser
                fields = ("email", "date_of_birth")

            def __getattribute__(self, name):
                if name == "save_m2m":
                    raise AttributeError
                return super().__getattribute__(name)

        data = {
            "email": "hidden@example.com",
            "password1": "test123",
            "password2": "test123",
            "date_of_birth": "1980-12-12",
        }
        form = BrokenForm(data)
        self.assertTrue(form.is_valid())
        user = form.save(commit=True)
        # CustomUser uses email as username field; ensure saved
        self.assertEqual(user.email, "hidden@example.com")

    def test_hidden_save_m2m_with_m2m_field_present_does_not_error(self):
        # Create an organization for the M2M value
        org = Organization.objects.create(name="Org Hidden")
        class BrokenForm(UserCreationForm):
            class Meta(UserCreationForm.Meta):
                model = CustomUserWithM2M
                fields = UserCreationForm.Meta.fields + ("orgs",)

            def __getattribute__(self, name):
                if name == "save_m2m":
                    raise AttributeError
                return super().__getattribute__(name)

        data = {
            "username": "hidden_save_7",
            "password1": "test123",
            "password2": "test123",
            "orgs": [str(org.pk)],
        }
        form = BrokenForm(data)
        self.assertTrue(form.is_valid())
        user = form.save(commit=True)
        # save() must not raise even though save_m2m is hidden; orgs may not be saved
        self.assertEqual(user.username, "hidden_save_7")
        # Because save_m2m was hidden, the M2M may not be saved; ensure code didn't error and count is int
        self.assertIsInstance(user.orgs.count(), int)

    def test_hidden_save_m2m_multiple_saves(self):
        class BrokenForm(UserCreationForm):
            def __getattribute__(self, name):
                if name == "save_m2m":
                    raise AttributeError
                return super().__getattribute__(name)

        data = {"username": "hidden_save_8", "password1": "test123", "password2": "test123"}
        form = BrokenForm(data)
        self.assertTrue(form.is_valid())
        user = form.save(commit=True)
        # Calling save again (simulating subsequent saves) should also not raise
        user.username = "hidden_save_8b"
        user.save()
        self.assertEqual(User.objects.get(pk=user.pk).username, "hidden_save_8b")

    def test_hidden_save_m2m_preserves_password_whitespace(self):
        class BrokenForm(UserCreationForm):
            def __getattribute__(self, name):
                if name == "save_m2m":
                    raise AttributeError
                return super().__getattribute__(name)

        data = {"username": "hidden_save_9", "password1": "  pass  ", "password2": "  pass  "}
        form = BrokenForm(data)
        self.assertTrue(form.is_valid())
        user = form.save(commit=True)
        # Ensure whitespace in password is preserved when set
        self.assertTrue(user.check_password("  pass  "))

    def test_hidden_save_m2m_with_i18n_context(self):
        class BrokenForm(UserCreationForm):
            def __getattribute__(self, name):
                if name == "save_m2m":
                    raise AttributeError
                return super().__getattribute__(name)

        # Run inside a translation override to ensure no side-effects with i18n
        with translation.override("fr"):
            data = {"username": "hidden_save_10", "password1": "test123", "password2": "test123"}
            form = BrokenForm(data)
            self.assertTrue(form.is_valid())
            user = form.save(commit=True)
        self.assertEqual(User.objects.get(username="hidden_save_10"), user)