from unittest import mock
from django.contrib.auth.models import User
from django.db import DatabaseError, router
from django.test import TestCase, override_settings
from django.urls import reverse
from admin_changelist.models import Swallow

@override_settings(ROOT_URLCONF='admin_changelist.urls')
class ChangeListAtomicUsingArgTests(TestCase):

    def _base_post_data(self):
        return {'form-TOTAL_FORMS': '3', 'form-INITIAL_FORMS': '3', 'form-MIN_NUM_FORMS': '0', 'form-MAX_NUM_FORMS': '1000', 'form-0-uuid': str(self.a.pk), 'form-1-uuid': str(self.b.pk), 'form-2-uuid': str(self.c.pk), '_save': 'Save'}

    def test_atomic_called_with_using_on_single_form_change(self):
        data = self._base_post_data()
        data.update({'form-0-load': '9.0', 'form-0-speed': '3.0', 'form-1-load': '2.0', 'form-1-speed': '2.0', 'form-2-load': '5.0', 'form-2-speed': '5.0'})
        with mock.patch('django.contrib.admin.options.transaction.atomic') as atomic_mock:
            response = self.client.post(self.changelist_url, data)
            self._assert_atomic_called_with_using_for_model(atomic_mock, Swallow)

    def test_atomic_called_with_using_even_if_no_forms_changed(self):
        data = self._base_post_data()
        data.update({'form-0-load': str(self.a.load), 'form-0-speed': str(self.a.speed), 'form-1-load': str(self.b.load), 'form-1-speed': str(self.b.speed), 'form-2-load': str(self.c.load), 'form-2-speed': str(self.c.speed)})
        with mock.patch('django.contrib.admin.options.transaction.atomic') as atomic_mock:
            response = self.client.post(self.changelist_url, data)
            self._assert_atomic_called_with_using_for_model(atomic_mock, Swallow)

    def test_atomic_called_with_using_on_multiple_forms_changed(self):
        data = self._base_post_data()
        data.update({'form-0-load': '9.0', 'form-0-speed': '3.0', 'form-1-load': '5.0', 'form-1-speed': '4.0', 'form-2-load': '7.0', 'form-2-speed': '6.0'})
        with mock.patch('django.contrib.admin.options.transaction.atomic') as atomic_mock:
            response = self.client.post(self.changelist_url, data)
            self._assert_atomic_called_with_using_for_model(atomic_mock, Swallow)

from django.test import TestCase, override_settings
from django.urls import reverse
from django.db import DatabaseError
from unittest import mock
from .models import Swallow
from .admin import SwallowAdmin
from django.contrib.admin.options import router

@override_settings(ROOT_URLCONF='admin_changelist.urls')
class TransactionAtomicUsageTests(TestCase):

    def test_atomic_called_when_no_form_changed(self):
        a = Swallow.objects.create(origin='A', load=1, speed=1)
        b = Swallow.objects.create(origin='B', load=2, speed=2)
        data = {'form-TOTAL_FORMS': '2', 'form-INITIAL_FORMS': '2', 'form-MIN_NUM_FORMS': '0', 'form-MAX_NUM_FORMS': '1000', 'form-0-uuid': str(a.pk), 'form-0-load': str(float(a.load)), 'form-0-speed': str(float(a.speed)), 'form-1-uuid': str(b.pk), 'form-1-load': str(float(b.load)), 'form-1-speed': str(float(b.speed)), '_save': 'Save'}
        with mock.patch('django.contrib.admin.options.transaction.atomic') as mock_atomic:
            with mock.patch('django.contrib.admin.options.router.db_for_write', return_value='mydb') as mock_db_for_write:
                response = self.client.post(self.changelist_url, data)
                mock_atomic.assert_called_with(using='mydb')
                mock_db_for_write.assert_called_with(Swallow)

from django.db import router

@skipUnlessDBFeature('supports_transactions')
def test_atomic_used_on_list_editable_success(self):
    a = Swallow.objects.create(origin='Swallow A', load=4, speed=1)
    b = Swallow.objects.create(origin='Swallow B', load=2, speed=2)
    self.client.force_login(self.superuser)
    changelist_url = reverse('admin:admin_changelist_swallow_changelist')
    data = {'form-TOTAL_FORMS': '2', 'form-INITIAL_FORMS': '2', 'form-MIN_NUM_FORMS': '0', 'form-MAX_NUM_FORMS': '1000', 'form-0-uuid': str(a.pk), 'form-1-uuid': str(b.pk), 'form-0-load': '9.0', 'form-0-speed': '3.0', 'form-1-load': '5.0', 'form-1-speed': '1.0', '_save': 'Save'}
    expected_db = router.db_for_write(Swallow)
    with mock.patch('django.db.transaction.atomic') as mock_atomic:
        mock_atomic.return_value.__enter__.return_value = None
        mock_atomic.return_value.__exit__.return_value = None
        response = self.client.post(changelist_url, data)
    mock_atomic.assert_any_call(using=expected_db)

@skipUnlessDBFeature('supports_transactions')
def test_atomic_used_when_multiple_forms_changed(self):
    a = Swallow.objects.create(origin='Swallow A', load=4, speed=1)
    b = Swallow.objects.create(origin='Swallow B', load=2, speed=2)
    c = Swallow.objects.create(origin='Swallow C', load=5, speed=5)
    self.client.force_login(self.superuser)
    changelist_url = reverse('admin:admin_changelist_swallow_changelist')
    data = {'form-TOTAL_FORMS': '3', 'form-INITIAL_FORMS': '3', 'form-MIN_NUM_FORMS': '0', 'form-MAX_NUM_FORMS': '1000', 'form-0-uuid': str(a.pk), 'form-0-load': '9.0', 'form-0-speed': '3.0', 'form-1-uuid': str(b.pk), 'form-1-load': '5.0', 'form-1-speed': '1.0', 'form-2-uuid': str(c.pk), 'form-2-load': '6.0', 'form-2-speed': '2.0', '_save': 'Save'}
    expected_db = router.db_for_write(Swallow)
    with mock.patch('django.db.transaction.atomic') as mock_atomic:
        mock_atomic.return_value.__enter__.return_value = None
        mock_atomic.return_value.__exit__.return_value = None
        response = self.client.post(changelist_url, data)
    mock_atomic.assert_any_call(using=expected_db)

@skipUnlessDBFeature('supports_transactions')
def test_atomic_used_even_if_no_forms_changed(self):
    a = Swallow.objects.create(origin='Swallow A', load=4, speed=1)
    b = Swallow.objects.create(origin='Swallow B', load=2, speed=2)
    self.client.force_login(self.superuser)
    changelist_url = reverse('admin:admin_changelist_swallow_changelist')
    data = {'form-TOTAL_FORMS': '2', 'form-INITIAL_FORMS': '2', 'form-MIN_NUM_FORMS': '0', 'form-MAX_NUM_FORMS': '1000', 'form-0-uuid': str(a.pk), 'form-1-uuid': str(b.pk), 'form-0-load': str(a.load), 'form-0-speed': str(a.speed), 'form-1-load': str(b.load), 'form-1-speed': str(b.speed), '_save': 'Save'}
    expected_db = router.db_for_write(Swallow)
    with mock.patch('django.db.transaction.atomic') as mock_atomic:
        mock_atomic.return_value.__enter__.return_value = None
        mock_atomic.return_value.__exit__.return_value = None
        response = self.client.post(changelist_url, data)
    mock_atomic.assert_any_call(using=expected_db)

@skipUnlessDBFeature('supports_transactions')
def test_atomic_not_used_when_formset_invalid(self):
    a = Swallow.objects.create(origin='Swallow A', load=4, speed=1)
    b = Swallow.objects.create(origin='Swallow B', load=2, speed=2)
    self.client.force_login(self.superuser)
    changelist_url = reverse('admin:admin_changelist_swallow_changelist')
    data = {'form-TOTAL_FORMS': '2', 'form-INITIAL_FORMS': '2', 'form-MIN_NUM_FORMS': '0', 'form-MAX_NUM_FORMS': '1000', 'form-0-uuid': str(a.pk), 'form-0-load': 'not-a-number', 'form-0-speed': '3.0', 'form-1-uuid': str(b.pk), 'form-1-load': 'also-invalid', 'form-1-speed': '1.0', '_save': 'Save'}
    with mock.patch('django.db.transaction.atomic') as mock_atomic:
        mock_atomic.return_value.__enter__.return_value = None
        mock_atomic.return_value.__exit__.return_value = None
        response = self.client.post(changelist_url, data)
    mock_atomic.assert_not_called()

@skipUnlessDBFeature('supports_transactions')
def test_atomic_used_when_save_model_raises(self):
    a = Swallow.objects.create(origin='Swallow A', load=4, speed=1)
    b = Swallow.objects.create(origin='Swallow B', load=2, speed=2)
    self.client.force_login(self.superuser)
    changelist_url = reverse('admin:admin_changelist_swallow_changelist')
    data = {'form-TOTAL_FORMS': '2', 'form-INITIAL_FORMS': '2', 'form-MIN_NUM_FORMS': '0', 'form-MAX_NUM_FORMS': '1000', 'form-0-uuid': str(a.pk), 'form-0-load': '9.0', 'form-0-speed': '3.0', 'form-1-uuid': str(b.pk), 'form-1-load': '5.0', 'form-1-speed': '1.0', '_save': 'Save'}
    expected_db = router.db_for_write(Swallow)
    with mock.patch('django.contrib.admin.ModelAdmin.save_model', side_effect=DatabaseError):
        with mock.patch('django.db.transaction.atomic') as mock_atomic:
            mock_atomic.return_value.__enter__.return_value = None
            mock_atomic.return_value.__exit__.return_value = None
            with self.assertRaises(DatabaseError):
                self.client.post(changelist_url, data)
    mock_atomic.assert_any_call(using=expected_db)

@skipUnlessDBFeature('supports_transactions')
def test_atomic_used_when_save_related_raises(self):
    a = Swallow.objects.create(origin='Swallow A', load=4, speed=1)
    b = Swallow.objects.create(origin='Swallow B', load=2, speed=2)
    self.client.force_login(self.superuser)
    changelist_url = reverse('admin:admin_changelist_swallow_changelist')
    data = {'form-TOTAL_FORMS': '2', 'form-INITIAL_FORMS': '2', 'form-MIN_NUM_FORMS': '0', 'form-MAX_NUM_FORMS': '1000', 'form-0-uuid': str(a.pk), 'form-0-load': '9.0', 'form-0-speed': '3.0', 'form-1-uuid': str(b.pk), 'form-1-load': '5.0', 'form-1-speed': '1.0', '_save': 'Save'}
    expected_db = router.db_for_write(Swallow)
    with mock.patch('django.contrib.admin.ModelAdmin.save_related', side_effect=DatabaseError):
        with mock.patch('django.db.transaction.atomic') as mock_atomic:
            mock_atomic.return_value.__enter__.return_value = None
            mock_atomic.return_value.__exit__.return_value = None
            with self.assertRaises(DatabaseError):
                self.client.post(changelist_url, data)
    mock_atomic.assert_any_call(using=expected_db)

@skipUnlessDBFeature('supports_transactions')
def test_atomic_used_when_save_form_raises(self):
    a = Swallow.objects.create(origin='Swallow A', load=4, speed=1)
    b = Swallow.objects.create(origin='Swallow B', load=2, speed=2)
    self.client.force_login(self.superuser)
    changelist_url = reverse('admin:admin_changelist_swallow_changelist')
    data = {'form-TOTAL_FORMS': '2', 'form-INITIAL_FORMS': '2', 'form-MIN_NUM_FORMS': '0', 'form-MAX_NUM_FORMS': '1000', 'form-0-uuid': str(a.pk), 'form-0-load': '9.0', 'form-0-speed': '3.0', 'form-1-uuid': str(b.pk), 'form-1-load': '5.0', 'form-1-speed': '1.0', '_save': 'Save'}
    expected_db = router.db_for_write(Swallow)
    with mock.patch('django.contrib.admin.ModelAdmin.save_form', side_effect=DatabaseError):
        with mock.patch('django.db.transaction.atomic') as mock_atomic:
            mock_atomic.return_value.__enter__.return_value = None
            mock_atomic.return_value.__exit__.return_value = None
            with self.assertRaises(DatabaseError):
                self.client.post(changelist_url, data)
    mock_atomic.assert_any_call(using=expected_db)

@skipUnlessDBFeature('supports_transactions')
def test_atomic_used_when_log_change_raises(self):
    a = Swallow.objects.create(origin='Swallow A', load=4, speed=1)
    b = Swallow.objects.create(origin='Swallow B', load=2, speed=2)
    self.client.force_login(self.superuser)
    changelist_url = reverse('admin:admin_changelist_swallow_changelist')
    data = {'form-TOTAL_FORMS': '2', 'form-INITIAL_FORMS': '2', 'form-MIN_NUM_FORMS': '0', 'form-MAX_NUM_FORMS': '1000', 'form-0-uuid': str(a.pk), 'form-0-load': '9.0', 'form-0-speed': '3.0', 'form-1-uuid': str(b.pk), 'form-1-load': '5.0', 'form-1-speed': '1.0', '_save': 'Save'}
    expected_db = router.db_for_write(Swallow)
    with mock.patch('django.contrib.admin.ModelAdmin.log_change', side_effect=DatabaseError):
        with mock.patch('django.db.transaction.atomic') as mock_atomic:
            mock_atomic.return_value.__enter__.return_value = None
            mock_atomic.return_value.__exit__.return_value = None
            with self.assertRaises(DatabaseError):
                self.client.post(changelist_url, data)
    mock_atomic.assert_any_call(using=expected_db)

@skipUnlessDBFeature('supports_transactions')
def test_atomic_respects_router_db_for_write_override(self):
    a = Swallow.objects.create(origin='Swallow A', load=4, speed=1)
    b = Swallow.objects.create(origin='Swallow B', load=2, speed=2)
    self.client.force_login(self.superuser)
    changelist_url = reverse('admin:admin_changelist_swallow_changelist')
    data = {'form-TOTAL_FORMS': '2', 'form-INITIAL_FORMS': '2', 'form-MIN_NUM_FORMS': '0', 'form-MAX_NUM_FORMS': '1000', 'form-0-uuid': str(a.pk), 'form-0-load': '9.0', 'form-0-speed': '3.0', 'form-1-uuid': str(b.pk), 'form-1-load': '5.0', 'form-1-speed': '1.0', '_save': 'Save'}
    with mock.patch('django.db.router.db_for_write', return_value='custom_db'):
        with mock.patch('django.db.transaction.atomic') as mock_atomic:
            mock_atomic.return_value.__enter__.return_value = None
            mock_atomic.return_value.__exit__.return_value = None
            response = self.client.post(changelist_url, data)
    mock_atomic.assert_any_call(using='custom_db')

@skipUnlessDBFeature('supports_transactions')
def test_changelist_atomic_uses_router_db_for_simple_save(self):
    a = Swallow.objects.create(origin='Swallow A', load=4, speed=1)
    b = Swallow.objects.create(origin='Swallow B', load=2, speed=2)
    superuser = self._create_superuser('superuser')
    self.client.force_login(superuser)
    changelist_url = reverse('admin:admin_changelist_swallow_changelist')
    data = {'form-TOTAL_FORMS': '2', 'form-INITIAL_FORMS': '2', 'form-MIN_NUM_FORMS': '0', 'form-MAX_NUM_FORMS': '1000', 'form-0-uuid': str(a.pk), 'form-1-uuid': str(b.pk), 'form-0-load': '9.0', 'form-0-speed': '3.0', 'form-1-load': '5.0', 'form-1-speed': '1.0', '_save': 'Save'}
    with mock.patch('django.db.router.db_for_write') as mock_db_for_write, mock.patch('django.db.transaction.atomic') as mock_atomic:
        mock_db_for_write.return_value = 'other'
        cm = mock.MagicMock()
        cm.__enter__.return_value = None
        cm.__exit__.return_value = False
        mock_atomic.return_value = cm
        response = self.client.post(changelist_url, data)
        mock_db_for_write.assert_called_with(Swallow)
        mock_atomic.assert_called_with(using='other')

@skipUnlessDBFeature('supports_transactions')
def test_changelist_atomic_called_even_if_no_forms_changed(self):
    a = Swallow.objects.create(origin='Swallow A', load=4, speed=1)
    b = Swallow.objects.create(origin='Swallow B', load=2, speed=2)
    superuser = self._create_superuser('superuser')
    self.client.force_login(superuser)
    changelist_url = reverse('admin:admin_changelist_swallow_changelist')
    data = {'form-TOTAL_FORMS': '2', 'form-INITIAL_FORMS': '2', 'form-MIN_NUM_FORMS': '0', 'form-MAX_NUM_FORMS': '1000', 'form-0-uuid': str(a.pk), 'form-1-uuid': str(b.pk), 'form-0-load': str(a.load), 'form-0-speed': str(a.speed), 'form-1-load': str(b.load), 'form-1-speed': str(b.speed), '_save': 'Save'}
    with mock.patch('django.db.router.db_for_write') as mock_db_for_write, mock.patch('django.db.transaction.atomic') as mock_atomic:
        mock_db_for_write.return_value = 'other'
        cm = mock.MagicMock()
        cm.__enter__.return_value = None
        cm.__exit__.return_value = False
        mock_atomic.return_value = cm
        response = self.client.post(changelist_url, data)
        mock_db_for_write.assert_called_with(Swallow)
        mock_atomic.assert_called_with(using='other')

@skipUnlessDBFeature('supports_transactions')
def test_changelist_atomic_called_with_ordering_param(self):
    a = Swallow.objects.create(origin='Swallow A', load=4, speed=1)
    b = Swallow.objects.create(origin='Swallow B', load=2, speed=2)
    superuser = self._create_superuser('superuser')
    self.client.force_login(superuser)
    changelist_url = reverse('admin:admin_changelist_swallow_changelist') + '?o=-2'
    data = {'form-TOTAL_FORMS': '2', 'form-INITIAL_FORMS': '2', 'form-MIN_NUM_FORMS': '0', 'form-MAX_NUM_FORMS': '1000', 'form-0-uuid': str(a.pk), 'form-1-uuid': str(b.pk), 'form-0-load': '9.0', 'form-0-speed': '3.0', 'form-1-load': '5.0', 'form-1-speed': '1.0', '_save': 'Save'}
    with mock.patch('django.db.router.db_for_write') as mock_db_for_write, mock.patch('django.db.transaction.atomic') as mock_atomic:
        mock_db_for_write.return_value = 'other'
        cm = mock.MagicMock()
        cm.__enter__.return_value = None
        cm.__exit__.return_value = False
        mock_atomic.return_value = cm
        response = self.client.post(changelist_url, data)
        mock_db_for_write.assert_called_with(Swallow)
        mock_atomic.assert_called_with(using='other')

@skipUnlessDBFeature('supports_transactions')
def test_changelist_atomic_used_when_log_change_raises(self):
    a = Swallow.objects.create(origin='Swallow A', load=4, speed=1)
    b = Swallow.objects.create(origin='Swallow B', load=2, speed=2)
    superuser = self._create_superuser('superuser')
    self.client.force_login(superuser)
    changelist_url = reverse('admin:admin_changelist_swallow_changelist')
    data = {'form-TOTAL_FORMS': '2', 'form-INITIAL_FORMS': '2', 'form-MIN_NUM_FORMS': '0', 'form-MAX_NUM_FORMS': '1000', 'form-0-uuid': str(a.pk), 'form-1-uuid': str(b.pk), 'form-0-load': '9.0', 'form-0-speed': '3.0', 'form-1-load': '5.0', 'form-1-speed': '1.0', '_save': 'Save'}
    with mock.patch('django.db.router.db_for_write') as mock_db_for_write, mock.patch('django.db.transaction.atomic') as mock_atomic, mock.patch('django.contrib.admin.ModelAdmin.log_change', side_effect=DatabaseError):
        mock_db_for_write.return_value = 'other'
        cm = mock.MagicMock()
        cm.__enter__.return_value = None
        cm.__exit__.return_value = False
        mock_atomic.return_value = cm
        with self.assertRaises(DatabaseError):
            self.client.post(changelist_url, data)
        mock_db_for_write.assert_called_with(Swallow)
        mock_atomic.assert_called_with(using='other')

@skipUnlessDBFeature('supports_transactions')
def test_changelist_atomic_called_when_log_change_raises_on_second(self):
    a = Swallow.objects.create(origin='Swallow A', load=4, speed=1)
    b = Swallow.objects.create(origin='Swallow B', load=2, speed=2)
    superuser = self._create_superuser('superuser')
    self.client.force_login(superuser)
    changelist_url = reverse('admin:admin_changelist_swallow_changelist')
    data = {'form-TOTAL_FORMS': '2', 'form-INITIAL_FORMS': '2', 'form-MIN_NUM_FORMS': '0', 'form-MAX_NUM_FORMS': '1000', 'form-0-uuid': str(a.pk), 'form-1-uuid': str(b.pk), 'form-0-load': '9.0', 'form-0-speed': '3.0', 'form-1-load': '5.0', 'form-1-speed': '1.0', '_save': 'Save'}
    with mock.patch('django.db.router.db_for_write') as mock_db_for_write, mock.patch('django.db.transaction.atomic') as mock_atomic, mock.patch('django.contrib.admin.ModelAdmin.log_change', side_effect=[None, DatabaseError]):
        mock_db_for_write.return_value = 'other'
        cm = mock.MagicMock()
        cm.__enter__.return_value = None
        cm.__exit__.return_value = False
        mock_atomic.return_value = cm
        with self.assertRaises(DatabaseError):
            self.client.post(changelist_url, data)
        mock_db_for_write.assert_called_with(Swallow)
        mock_atomic.assert_called_with(using='other')

@skipUnlessDBFeature('supports_transactions')
def test_changelist_atomic_called_with_single_form(self):
    a = Swallow.objects.create(origin='Swallow A', load=4, speed=1)
    superuser = self._create_superuser('superuser')
    self.client.force_login(superuser)
    changelist_url = reverse('admin:admin_changelist_swallow_changelist')
    data = {'form-TOTAL_FORMS': '1', 'form-INITIAL_FORMS': '1', 'form-MIN_NUM_FORMS': '0', 'form-MAX_NUM_FORMS': '1000', 'form-0-uuid': str(a.pk), 'form-0-load': '10.0', 'form-0-speed': '3.0', '_save': 'Save'}
    with mock.patch('django.db.router.db_for_write') as mock_db_for_write, mock.patch('django.db.transaction.atomic') as mock_atomic:
        mock_db_for_write.return_value = 'other'
        cm = mock.MagicMock()
        cm.__enter__.return_value = None
        cm.__exit__.return_value = False
        mock_atomic.return_value = cm
        response = self.client.post(changelist_url, data)
        mock_db_for_write.assert_called_with(Swallow)
        mock_atomic.assert_called_with(using='other')

@skipUnlessDBFeature('supports_transactions')
def test_changelist_atomic_called_with_three_forms(self):
    a = Swallow.objects.create(origin='Swallow A', load=4, speed=1)
    b = Swallow.objects.create(origin='Swallow B', load=2, speed=2)
    c = Swallow.objects.create(origin='Swallow C', load=5, speed=5)
    superuser = self._create_superuser('superuser')
    self.client.force_login(superuser)
    changelist_url = reverse('admin:admin_changelist_swallow_changelist')
    data = {'form-TOTAL_FORMS': '3', 'form-INITIAL_FORMS': '3', 'form-MIN_NUM_FORMS': '0', 'form-MAX_NUM_FORMS': '1000', 'form-0-uuid': str(a.pk), 'form-1-uuid': str(b.pk), 'form-2-uuid': str(c.pk), 'form-0-load': '9.0', 'form-0-speed': '3.0', 'form-1-load': '5.0', 'form-1-speed': '1.0', 'form-2-load': '6.0', 'form-2-speed': '2.0', '_save': 'Save'}
    with mock.patch('django.db.router.db_for_write') as mock_db_for_write, mock.patch('django.db.transaction.atomic') as mock_atomic:
        mock_db_for_write.return_value = 'other'
        cm = mock.MagicMock()
        cm.__enter__.return_value = None
        cm.__exit__.return_value = False
        mock_atomic.return_value = cm
        response = self.client.post(changelist_url, data)
        mock_db_for_write.assert_called_with(Swallow)
        mock_atomic.assert_called_with(using='other')

@skipUnlessDBFeature('supports_transactions')
def test_changelist_atomic_called_with_extra_post_params(self):
    a = Swallow.objects.create(origin='Swallow A', load=4, speed=1)
    b = Swallow.objects.create(origin='Swallow B', load=2, speed=2)
    superuser = self._create_superuser('superuser')
    self.client.force_login(superuser)
    changelist_url = reverse('admin:admin_changelist_swallow_changelist')
    data = {'form-TOTAL_FORMS': '2', 'form-INITIAL_FORMS': '2', 'form-MIN_NUM_FORMS': '0', 'form-MAX_NUM_FORMS': '1000', 'form-0-uuid': str(a.pk), 'form-1-uuid': str(b.pk), 'form-0-load': '9.0', 'form-0-speed': '3.0', 'form-1-load': '5.0', 'form-1-speed': '1.0', 'some-other-param': 'value', '_save': 'Save'}
    with mock.patch('django.db.router.db_for_write') as mock_db_for_write, mock.patch('django.db.transaction.atomic') as mock_atomic:
        mock_db_for_write.return_value = 'other'
        cm = mock.MagicMock()
        cm.__enter__.return_value = None
        cm.__exit__.return_value = False
        mock_atomic.return_value = cm
        response = self.client.post(changelist_url, data)
        mock_db_for_write.assert_called_with(Swallow)
        mock_atomic.assert_called_with(using='other')

@skipUnlessDBFeature('supports_transactions')
def test_changelist_atomic_called_when_action_selected_but_saving_list_editable(self):
    a = Swallow.objects.create(origin='Swallow A', load=4, speed=1)
    b = Swallow.objects.create(origin='Swallow B', load=2, speed=2)
    superuser = self._create_superuser('superuser')
    self.client.force_login(superuser)
    changelist_url = reverse('admin:admin_changelist_swallow_changelist')
    data = {'form-TOTAL_FORMS': '2', 'form-INITIAL_FORMS': '2', 'form-MIN_NUM_FORMS': '0', 'form-MAX_NUM_FORMS': '1000', 'form-0-uuid': str(a.pk), 'form-1-uuid': str(b.pk), 'form-0-load': '9.0', 'form-0-speed': '3.0', 'form-1-load': '5.0', 'form-1-speed': '1.0', 'action': 'delete_selected', '_save': 'Save'}
    with mock.patch('django.db.router.db_for_write') as mock_db_for_write, mock.patch('django.db.transaction.atomic') as mock_atomic:
        mock_db_for_write.return_value = 'other'
        cm = mock.MagicMock()
        cm.__enter__.return_value = None
        cm.__exit__.return_value = False
        mock_atomic.return_value = cm
        response = self.client.post(changelist_url, data)
        mock_db_for_write.assert_called_with(Swallow)
        mock_atomic.assert_called_with(using='other')

from django.db import router

@skipUnlessDBFeature('supports_transactions')
def test_atomic_used_with_swallow_admin(self):
    a = Swallow.objects.create(origin='Swallow A', load=4, speed=1)
    b = Swallow.objects.create(origin='Swallow B', load=2, speed=2)
    self.client.force_login(self.superuser)
    changelist_url = reverse('admin:admin_changelist_swallow_changelist')
    data = {'form-TOTAL_FORMS': '2', 'form-INITIAL_FORMS': '2', 'form-MIN_NUM_FORMS': '0', 'form-MAX_NUM_FORMS': '1000', 'form-0-uuid': str(a.pk), 'form-0-load': '9.0', 'form-0-speed': '3.0', 'form-1-uuid': str(b.pk), 'form-1-load': '5.0', 'form-1-speed': '1.0', '_save': 'Save'}
    with mock.patch('django.contrib.admin.options.transaction.atomic') as atomic:
        response = self.client.post(changelist_url, data)
    calls = atomic.call_args_list
    self.assertTrue(any((call[1].get('using') == router.db_for_write(Swallow) for call in calls)), 'transaction.atomic must be called with using=router.db_for_write(Swallow)')

@skipUnlessDBFeature('supports_transactions')
def test_atomic_used_with_swallow_admin_multiple_changes(self):
    a = Swallow.objects.create(origin='Swallow A', load=4, speed=1)
    b = Swallow.objects.create(origin='Swallow B', load=2, speed=2)
    c = Swallow.objects.create(origin='Swallow C', load=5, speed=5)
    self.client.force_login(self.superuser)
    changelist_url = reverse('admin:admin_changelist_swallow_changelist')
    data = {'form-TOTAL_FORMS': '3', 'form-INITIAL_FORMS': '3', 'form-MIN_NUM_FORMS': '0', 'form-MAX_NUM_FORMS': '1000', 'form-0-uuid': str(a.pk), 'form-0-load': '8.0', 'form-0-speed': '2.0', 'form-1-uuid': str(b.pk), 'form-1-load': '6.0', 'form-1-speed': '1.0', 'form-2-uuid': str(c.pk), 'form-2-load': '5.0', 'form-2-speed': '4.0', '_save': 'Save'}
    with mock.patch('django.contrib.admin.options.transaction.atomic') as atomic:
        response = self.client.post(changelist_url, data)
    calls = atomic.call_args_list
    self.assertTrue(any((call[1].get('using') == router.db_for_write(Swallow) for call in calls)), 'transaction.atomic must be called with using=router.db_for_write(Swallow)')

@skipUnlessDBFeature('supports_transactions')
def test_atomic_used_when_log_change_raises(self):
    a = Swallow.objects.create(origin='Swallow A', load=4, speed=1)
    b = Swallow.objects.create(origin='Swallow B', load=2, speed=2)
    self.client.force_login(self.superuser)
    changelist_url = reverse('admin:admin_changelist_swallow_changelist')
    data = {'form-TOTAL_FORMS': '2', 'form-INITIAL_FORMS': '2', 'form-MIN_NUM_FORMS': '0', 'form-MAX_NUM_FORMS': '1000', 'form-0-uuid': str(a.pk), 'form-0-load': '9.0', 'form-0-speed': '3.0', 'form-1-uuid': str(b.pk), 'form-1-load': '5.0', 'form-1-speed': '1.0', '_save': 'Save'}
    with mock.patch('django.contrib.admin.ModelAdmin.log_change', side_effect=DatabaseError):
        with mock.patch('django.contrib.admin.options.transaction.atomic') as atomic:
            with self.assertRaises(DatabaseError):
                self.client.post(changelist_url, data)
    calls = atomic.call_args_list
    self.assertTrue(any((call[1].get('using') == router.db_for_write(Swallow) for call in calls)), 'transaction.atomic must be called with using=router.db_for_write(Swallow) even when exceptions occur')

@skipUnlessDBFeature('supports_transactions')
def test_atomic_used_with_child_admin_via_factory(self):
    parent = Parent.objects.create(name='Parent X')
    c1 = Child.objects.create(name='c1', parent=parent)
    c2 = Child.objects.create(name='c2', parent=parent)
    m = ChildAdmin(Child, custom_site)
    m.list_display = ['id', 'name', 'parent']
    m.list_display_links = ['id']
    m.list_editable = ['name']
    request = self.factory.post(reverse('admin:admin_changelist_child_changelist'), data={'form-TOTAL_FORMS': '2', 'form-INITIAL_FORMS': '2', 'form-MIN_NUM_FORMS': '0', 'form-MAX_NUM_FORMS': '1000', 'form-0-id': str(c1.pk), 'form-0-name': 'newc1', 'form-1-id': str(c2.pk), 'form-1-name': 'newc2', '_save': 'Save'})
    request.user = self.superuser
    request._messages = CookieStorage(request)
    with mock.patch('django.contrib.admin.options.transaction.atomic') as atomic:
        m.changelist_view(request)
    calls = atomic.call_args_list
    self.assertTrue(any((call[1].get('using') == router.db_for_write(Child) for call in calls)), 'transaction.atomic must be called with using=router.db_for_write(Child)')

@skipUnlessDBFeature('supports_transactions')
def test_atomic_used_with_child_admin_multiple_forms(self):
    parent = Parent.objects.create(name='Parent Y')
    c1 = Child.objects.create(name='c1', parent=parent)
    c2 = Child.objects.create(name='c2', parent=parent)
    c3 = Child.objects.create(name='c3', parent=parent)
    m = ChildAdmin(Child, custom_site)
    m.list_display = ['id', 'name', 'parent']
    m.list_display_links = ['id']
    m.list_editable = ['name']
    request = self.factory.post(reverse('admin:admin_changelist_child_changelist'), data={'form-TOTAL_FORMS': '3', 'form-INITIAL_FORMS': '3', 'form-MIN_NUM_FORMS': '0', 'form-MAX_NUM_FORMS': '1000', 'form-0-id': str(c1.pk), 'form-0-name': 'nc1', 'form-1-id': str(c2.pk), 'form-1-name': 'nc2', 'form-2-id': str(c3.pk), 'form-2-name': 'nc3', '_save': 'Save'})
    request.user = self.superuser
    request._messages = CookieStorage(request)
    with mock.patch('django.contrib.admin.options.transaction.atomic') as atomic:
        m.changelist_view(request)
    calls = atomic.call_args_list
    self.assertTrue(any((call[1].get('using') == router.db_for_write(Child) for call in calls)), 'transaction.atomic must be called with using=router.db_for_write(Child) for multiple edited forms')

@skipUnlessDBFeature('supports_transactions')
def test_atomic_used_with_group_admin(self):
    g1 = Group.objects.create(name='G1')
    g2 = Group.objects.create(name='G2')
    m = GroupAdmin(Group, custom_site)
    m.list_display = ['id', 'name']
    m.list_display_links = ['id']
    m.list_editable = ['name']
    request = self.factory.post(reverse('admin:admin_changelist_group_changelist'), data={'form-TOTAL_FORMS': '2', 'form-INITIAL_FORMS': '2', 'form-MIN_NUM_FORMS': '0', 'form-MAX_NUM_FORMS': '1000', 'form-0-id': str(g1.pk), 'form-0-name': 'New G1', 'form-1-id': str(g2.pk), 'form-1-name': 'New G2', '_save': 'Save'})
    request.user = self.superuser
    request._messages = CookieStorage(request)
    with mock.patch('django.contrib.admin.options.transaction.atomic') as atomic:
        m.changelist_view(request)
    calls = atomic.call_args_list
    self.assertTrue(any((call[1].get('using') == router.db_for_write(Group) for call in calls)), 'transaction.atomic must be called with using=router.db_for_write(Group)')

@skipUnlessDBFeature('supports_transactions')
def test_atomic_used_with_concert_admin(self):
    band = Group.objects.create(name='Band1')
    c1 = Concert.objects.create(name='C1', group=band)
    c2 = Concert.objects.create(name='C2', group=band)
    m = ConcertAdmin(Concert, custom_site)
    m.list_display = ['id', 'name', 'group']
    m.list_display_links = ['id']
    m.list_editable = ['name']
    request = self.factory.post(reverse('admin:admin_changelist_concert_changelist'), data={'form-TOTAL_FORMS': '2', 'form-INITIAL_FORMS': '2', 'form-MIN_NUM_FORMS': '0', 'form-MAX_NUM_FORMS': '1000', 'form-0-id': str(c1.pk), 'form-0-name': 'New C1', 'form-1-id': str(c2.pk), 'form-1-name': 'New C2', '_save': 'Save'})
    request.user = self.superuser
    request._messages = CookieStorage(request)
    with mock.patch('django.contrib.admin.options.transaction.atomic') as atomic:
        m.changelist_view(request)
    calls = atomic.call_args_list
    self.assertTrue(any((call[1].get('using') == router.db_for_write(Concert) for call in calls)), 'transaction.atomic must be called with using=router.db_for_write(Concert)')

@skipUnlessDBFeature('supports_transactions')
def test_atomic_used_with_band_admin(self):
    b1 = Band.objects.create(name='B1', nr_of_members=1)
    b2 = Band.objects.create(name='B2', nr_of_members=2)
    m = BandAdmin(Band, custom_site)
    m.list_display = ['id', 'name']
    m.list_display_links = ['id']
    m.list_editable = ['name']
    request = self.factory.post(reverse('admin:admin_changelist_band_changelist'), data={'form-TOTAL_FORMS': '2', 'form-INITIAL_FORMS': '2', 'form-MIN_NUM_FORMS': '0', 'form-MAX_NUM_FORMS': '1000', 'form-0-id': str(b1.pk), 'form-0-name': 'New B1', 'form-1-id': str(b2.pk), 'form-1-name': 'New B2', '_save': 'Save'})
    request.user = self.superuser
    request._messages = CookieStorage(request)
    with mock.patch('django.contrib.admin.options.transaction.atomic') as atomic:
        m.changelist_view(request)
    calls = atomic.call_args_list
    self.assertTrue(any((call[1].get('using') == router.db_for_write(Band) for call in calls)), 'transaction.atomic must be called with using=router.db_for_write(Band)')

@skipUnlessDBFeature('supports_transactions')
def test_atomic_used_with_parent_admin(self):
    p1 = Parent.objects.create(name='P1')
    p2 = Parent.objects.create(name='P2')
    m = ParentAdmin(Parent, custom_site)
    m.list_display = ['id', 'name']
    m.list_display_links = ['id']
    m.list_editable = ['name']
    request = self.factory.post(reverse('admin:admin_changelist_parent_changelist'), data={'form-TOTAL_FORMS': '2', 'form-INITIAL_FORMS': '2', 'form-MIN_NUM_FORMS': '0', 'form-MAX_NUM_FORMS': '1000', 'form-0-id': str(p1.pk), 'form-0-name': 'New P1', 'form-1-id': str(p2.pk), 'form-1-name': 'New P2', '_save': 'Save'})
    request.user = self.superuser
    request._messages = CookieStorage(request)
    with mock.patch('django.contrib.admin.options.transaction.atomic') as atomic:
        m.changelist_view(request)
    calls = atomic.call_args_list
    self.assertTrue(any((call[1].get('using') == router.db_for_write(Parent) for call in calls)), 'transaction.atomic must be called with using=router.db_for_write(Parent)')

def _post_changelist_swallow(self, data, patch_db_for_write='other_db', side_effect=None):
    """
    Helper to POST changelist data for Swallow model while patching
    router.db_for_write and transaction.atomic.

    Returns the atomic mock used (so tests can inspect call args).
    """
    changelist_url = reverse('admin:admin_changelist_swallow_changelist')
    self.client.force_login(self.superuser)
    with mock.patch('django.db.router.db_for_write', return_value=patch_db_for_write):
        with mock.patch('django.db.transaction.atomic') as atomic_mock:
            atomic_cm = mock.MagicMock()
            atomic_mock.return_value = atomic_cm
            if side_effect is None:
                response = self.client.post(changelist_url, data)
            else:
                with mock.patch('django.contrib.admin.ModelAdmin.log_change', side_effect=side_effect):
                    response = None
                    try:
                        response = self.client.post(changelist_url, data)
                    finally:
                        pass
            return (atomic_mock, response)

def _make_swallow_data(self):
    a = Swallow.objects.create(origin='Swallow A', load=4, speed=1)
    b = Swallow.objects.create(origin='Swallow B', load=2, speed=2)
    data = {'form-TOTAL_FORMS': '2', 'form-INITIAL_FORMS': '2', 'form-MIN_NUM_FORMS': '0', 'form-MAX_NUM_FORMS': '1000', 'form-0-uuid': str(a.pk), 'form-0-load': '9.0', 'form-0-speed': '3.0', 'form-1-uuid': str(b.pk), 'form-1-load': '5.0', 'form-1-speed': '1.0', '_save': 'Save'}
    return (a, b, data)

def test_atomic_called_with_using_alias_on_list_editable_save(self):
    """transaction.atomic must be called with using=router.db_for_write(self.model)."""
    _, _, data = self._make_swallow_data()
    atomic_mock, response = self._post_changelist_swallow(data, patch_db_for_write='other_db')
    self.assertTrue(atomic_mock.called)
    self.assertIn('using', atomic_mock.call_args.kwargs)
    self.assertEqual(atomic_mock.call_args.kwargs['using'], 'other_db')

def test_atomic_called_with_using_when_log_change_raises(self):
    """Even when log_change raises, transaction.atomic must be called with the proper using arg."""
    _, _, data = self._make_swallow_data()
    atomic_mock, _ = self._post_changelist_swallow(data, patch_db_for_write='db_alias', side_effect=DatabaseError)
    self.assertTrue(atomic_mock.called)
    self.assertIn('using', atomic_mock.call_args.kwargs)
    self.assertEqual(atomic_mock.call_args.kwargs['using'], 'db_alias')

def test_atomic_called_with_using_for_default_alias(self):
    """router.db_for_write may return 'default' and atomic should be called with that alias."""
    _, _, data = self._make_swallow_data()
    atomic_mock, response = self._post_changelist_swallow(data, patch_db_for_write='default')
    self.assertTrue(atomic_mock.called)
    self.assertIn('using', atomic_mock.call_args.kwargs)
    self.assertEqual(atomic_mock.call_args.kwargs['using'], 'default')

def test_atomic_called_even_if_no_forms_changed(self):
    """
    If formset is valid but none of the forms have changed, the atomic
    context is still entered (transaction.atomic is used with using arg).
    """
    a = Swallow.objects.create(origin='Swallow A', load=4, speed=1)
    b = Swallow.objects.create(origin='Swallow B', load=2, speed=2)
    data = {'form-TOTAL_FORMS': '2', 'form-INITIAL_FORMS': '2', 'form-MIN_NUM_FORMS': '0', 'form-MAX_NUM_FORMS': '1000', 'form-0-uuid': str(a.pk), 'form-0-load': str(a.load), 'form-0-speed': str(a.speed), 'form-1-uuid': str(b.pk), 'form-1-load': str(b.load), 'form-1-speed': str(b.speed), '_save': 'Save'}
    atomic_mock, response = self._post_changelist_swallow(data, patch_db_for_write='x_db')
    self.assertTrue(atomic_mock.called)
    self.assertIn('using', atomic_mock.call_args.kwargs)
    self.assertEqual(atomic_mock.call_args.kwargs['using'], 'x_db')

def test_atomic_called_with_using_when_multiple_forms_and_second_log_change_raises(self):
    """
    When multiple forms are changed and the second log_change raises, atomic must
    still be invoked with the using kwarg so the whole operation can be rolled back.
    """
    a, b, data = self._make_swallow_data()
    with mock.patch('django.db.router.db_for_write', return_value='my_db'):
        with mock.patch('django.db.transaction.atomic') as atomic_mock:
            atomic_cm = mock.MagicMock()
            atomic_mock.return_value = atomic_cm
            with mock.patch('django.contrib.admin.ModelAdmin.log_change', side_effect=[None, DatabaseError]):
                with self.assertRaises(DatabaseError):
                    self.client.post(reverse('admin:admin_changelist_swallow_changelist'), data)
    self.assertTrue(atomic_mock.called)
    self.assertIn('using', atomic_mock.call_args.kwargs)
    self.assertEqual(atomic_mock.call_args.kwargs['using'], 'my_db')

def test_atomic_called_with_using_when_router_returns_none(self):
    """
    If router.db_for_write returns None, the atomic call should still receive
    a 'using' kwarg with value None (the gold patch passes the value through).
    """
    _, _, data = self._make_swallow_data()
    atomic_mock, response = self._post_changelist_swallow(data, patch_db_for_write=None)
    self.assertTrue(atomic_mock.called)
    self.assertIn('using', atomic_mock.call_args.kwargs)
    self.assertIsNone(atomic_mock.call_args.kwargs['using'])

def test_atomic_called_with_using_for_unusual_alias(self):
    """DB alias with special characters should be passed through to transaction.atomic."""
    _, _, data = self._make_swallow_data()
    weird_alias = 'other-db-alias'
    atomic_mock, response = self._post_changelist_swallow(data, patch_db_for_write=weird_alias)
    self.assertTrue(atomic_mock.called)
    self.assertIn('using', atomic_mock.call_args.kwargs)
    self.assertEqual(atomic_mock.call_args.kwargs['using'], weird_alias)

def test_atomic_called_with_using_when_save_model_raises(self):
    """
    Ensure that when save_model raises an exception, the atomic context is still
    entered and called with the correct using arg.
    """
    a, b, data = self._make_swallow_data()
    with mock.patch('django.db.router.db_for_write', return_value='save_db'):
        with mock.patch('django.db.transaction.atomic') as atomic_mock:
            atomic_cm = mock.MagicMock()
            atomic_mock.return_value = atomic_cm
            with mock.patch('django.contrib.admin.ModelAdmin.save_model', side_effect=DatabaseError):
                with self.assertRaises(DatabaseError):
                    self.client.post(reverse('admin:admin_changelist_swallow_changelist'), data)
    self.assertTrue(atomic_mock.called)
    self.assertIn('using', atomic_mock.call_args.kwargs)
    self.assertEqual(atomic_mock.call_args.kwargs['using'], 'save_db')

def test_atomic_called_once_per_list_editable_save(self):
    """
    The atomic context manager should be entered exactly once for the
    list_editable save operation.
    """
    _, _, data = self._make_swallow_data()
    with mock.patch('django.db.router.db_for_write', return_value='once_db'):
        with mock.patch('django.db.transaction.atomic') as atomic_mock:
            atomic_cm = mock.MagicMock()
            atomic_mock.return_value = atomic_cm
            self.client.post(reverse('admin:admin_changelist_swallow_changelist'), data)
    self.assertEqual(atomic_mock.call_count, 1)

@skipUnlessDBFeature('supports_transactions')
def test_atomic_called_with_using_on_list_editable_success(self):
    a = Swallow.objects.create(origin='Swallow A', load=4, speed=1)
    b = Swallow.objects.create(origin='Swallow B', load=2, speed=2)
    self.client.force_login(self.superuser)
    changelist_url = reverse('admin:admin_changelist_swallow_changelist')
    data = {'form-TOTAL_FORMS': '2', 'form-INITIAL_FORMS': '2', 'form-MIN_NUM_FORMS': '0', 'form-MAX_NUM_FORMS': '1000', 'form-0-uuid': str(a.pk), 'form-1-uuid': str(b.pk), 'form-0-load': '9.0', 'form-0-speed': '3.0', 'form-1-load': '5.0', 'form-1-speed': '1.0', '_save': 'Save'}
    atomic_cm = mock.MagicMock()
    atomic_cm.__enter__ = mock.MagicMock(return_value=None)
    atomic_cm.__exit__ = mock.MagicMock(return_value=None)
    atomic_mock = mock.MagicMock(return_value=atomic_cm)
    with mock.patch('django.contrib.admin.options.transaction.atomic', atomic_mock):
        with mock.patch('django.contrib.admin.options.router.db_for_write', return_value='other_db'):
            response = self.client.post(changelist_url, data)
            self.assertEqual(response.status_code, 200)
    atomic_mock.assert_called_once_with(using='other_db')

@skipUnlessDBFeature('supports_transactions')
def test_atomic_called_with_using_on_list_editable_when_log_change_raises(self):
    a = Swallow.objects.create(origin='Swallow A', load=4, speed=1)
    b = Swallow.objects.create(origin='Swallow B', load=2, speed=2)
    self.client.force_login(self.superuser)
    changelist_url = reverse('admin:admin_changelist_swallow_changelist')
    data = {'form-TOTAL_FORMS': '2', 'form-INITIAL_FORMS': '2', 'form-MIN_NUM_FORMS': '0', 'form-MAX_NUM_FORMS': '1000', 'form-0-uuid': str(a.pk), 'form-1-uuid': str(b.pk), 'form-0-load': '9.0', 'form-0-speed': '3.0', 'form-1-load': '5.0', 'form-1-speed': '1.0', '_save': 'Save'}
    atomic_cm = mock.MagicMock()
    atomic_cm.__enter__ = mock.MagicMock(return_value=None)
    atomic_cm.__exit__ = mock.MagicMock(return_value=None)
    atomic_mock = mock.MagicMock(return_value=atomic_cm)
    with mock.patch('django.contrib.admin.options.transaction.atomic', atomic_mock):
        with mock.patch('django.contrib.admin.options.router.db_for_write', return_value='other_db'):
            with mock.patch('django.contrib.admin.ModelAdmin.log_change', side_effect=DatabaseError):
                with self.assertRaises(DatabaseError):
                    self.client.post(changelist_url, data)
    atomic_mock.assert_called_once_with(using='other_db')

@skipUnlessDBFeature('supports_transactions')
def test_atomic_called_with_using_on_list_editable_when_save_model_raises(self):
    a = Swallow.objects.create(origin='Swallow A', load=4, speed=1)
    b = Swallow.objects.create(origin='Swallow B', load=2, speed=2)
    self.client.force_login(self.superuser)
    changelist_url = reverse('admin:admin_changelist_swallow_changelist')
    data = {'form-TOTAL_FORMS': '2', 'form-INITIAL_FORMS': '2', 'form-MIN_NUM_FORMS': '0', 'form-MAX_NUM_FORMS': '1000', 'form-0-uuid': str(a.pk), 'form-1-uuid': str(b.pk), 'form-0-load': '9.0', 'form-0-speed': '3.0', 'form-1-load': '5.0', 'form-1-speed': '1.0', '_save': 'Save'}
    atomic_cm = mock.MagicMock()
    atomic_cm.__enter__ = mock.MagicMock(return_value=None)
    atomic_cm.__exit__ = mock.MagicMock(return_value=None)
    atomic_mock = mock.MagicMock(return_value=atomic_cm)
    with mock.patch('django.contrib.admin.options.transaction.atomic', atomic_mock):
        with mock.patch('django.contrib.admin.options.router.db_for_write', return_value='other_db'):
            with mock.patch('django.contrib.admin.ModelAdmin.save_model', side_effect=DatabaseError):
                with self.assertRaises(DatabaseError):
                    self.client.post(changelist_url, data)
    atomic_mock.assert_called_once_with(using='other_db')

@skipUnlessDBFeature('supports_transactions')
def test_atomic_not_called_if_formset_invalid(self):
    a = Swallow.objects.create(origin='Swallow A', load=4, speed=1)
    b = Swallow.objects.create(origin='Swallow B', load=2, speed=2)
    self.client.force_login(self.superuser)
    changelist_url = reverse('admin:admin_changelist_swallow_changelist')
    data = {'form-TOTAL_FORMS': '2', 'form-INITIAL_FORMS': '2', 'form-MIN_NUM_FORMS': '0', 'form-MAX_NUM_FORMS': '1000', 'form-0-uuid': str(a.pk), 'form-1-uuid': str(b.pk), 'form-0-load': 'invalid-float', 'form-0-speed': '3.0', 'form-1-load': '5.0', 'form-1-speed': '1.0', '_save': 'Save'}
    atomic_cm = mock.MagicMock()
    atomic_cm.__enter__ = mock.MagicMock(return_value=None)
    atomic_cm.__exit__ = mock.MagicMock(return_value=None)
    atomic_mock = mock.MagicMock(return_value=atomic_cm)
    with mock.patch('django.contrib.admin.options.transaction.atomic', atomic_mock):
        with mock.patch('django.contrib.admin.options.router.db_for_write', return_value='other_db'):
            response = self.client.post(changelist_url, data)
            self.assertEqual(response.status_code, 200)
    atomic_mock.assert_not_called()

@skipUnlessDBFeature('supports_transactions')
def test_atomic_not_called_if_no_list_editable_configured(self):
    a = Swallow.objects.create(origin='Swallow A', load=4, speed=1)
    b = Swallow.objects.create(origin='Swallow B', load=2, speed=2)
    m = SwallowAdmin(Swallow, custom_site)
    m.list_editable = []
    request = self.factory.post(reverse('admin:admin_changelist_swallow_changelist'), data={'_save': 'Save'})
    request.user = self.superuser
    atomic_cm = mock.MagicMock()
    atomic_cm.__enter__ = mock.MagicMock(return_value=None)
    atomic_cm.__exit__ = mock.MagicMock(return_value=None)
    atomic_mock = mock.MagicMock(return_value=atomic_cm)
    with mock.patch('django.contrib.admin.options.transaction.atomic', atomic_mock):
        with mock.patch('django.contrib.admin.options.router.db_for_write', return_value='other_db'):
            response = m.changelist_view(request)
            self.assertEqual(response.status_code, 200)
    atomic_mock.assert_not_called()

@skipUnlessDBFeature('supports_transactions')
def test_atomic_called_once_for_multiple_changed_forms(self):
    a = Swallow.objects.create(origin='Swallow A', load=4, speed=1)
    b = Swallow.objects.create(origin='Swallow B', load=2, speed=2)
    c = Swallow.objects.create(origin='Swallow C', load=5, speed=5)
    self.client.force_login(self.superuser)
    changelist_url = reverse('admin:admin_changelist_swallow_changelist')
    data = {'form-TOTAL_FORMS': '3', 'form-INITIAL_FORMS': '3', 'form-MIN_NUM_FORMS': '0', 'form-MAX_NUM_FORMS': '1000', 'form-0-uuid': str(a.pk), 'form-1-uuid': str(b.pk), 'form-2-uuid': str(c.pk), 'form-0-load': '9.0', 'form-0-speed': '3.0', 'form-1-load': '5.0', 'form-1-speed': '1.0', 'form-2-load': '7.0', 'form-2-speed': '6.0', '_save': 'Save'}
    atomic_cm = mock.MagicMock()
    atomic_cm.__enter__ = mock.MagicMock(return_value=None)
    atomic_cm.__exit__ = mock.MagicMock(return_value=None)
    atomic_mock = mock.MagicMock(return_value=atomic_cm)
    with mock.patch('django.contrib.admin.options.transaction.atomic', atomic_mock):
        with mock.patch('django.contrib.admin.options.router.db_for_write', return_value='other_db'):
            response = self.client.post(changelist_url, data)
            self.assertEqual(response.status_code, 200)
    atomic_mock.assert_called_once_with(using='other_db')

@skipUnlessDBFeature('supports_transactions')
def test_atomic_uses_router_db_for_write_non_default_alias(self):
    a = Swallow.objects.create(origin='Swallow A', load=4, speed=1)
    b = Swallow.objects.create(origin='Swallow B', load=2, speed=2)
    self.client.force_login(self.superuser)
    changelist_url = reverse('admin:admin_changelist_swallow_changelist')
    data = {'form-TOTAL_FORMS': '2', 'form-INITIAL_FORMS': '2', 'form-MIN_NUM_FORMS': '0', 'form-MAX_NUM_FORMS': '1000', 'form-0-uuid': str(a.pk), 'form-1-uuid': str(b.pk), 'form-0-load': '9.0', 'form-0-speed': '3.0', 'form-1-load': '5.0', 'form-1-speed': '1.0', '_save': 'Save'}
    for alias in ('default', 'replica', 'other_db'):
        atomic_cm = mock.MagicMock()
        atomic_cm.__enter__ = mock.MagicMock(return_value=None)
        atomic_cm.__exit__ = mock.MagicMock(return_value=None)
        atomic_mock = mock.MagicMock(return_value=atomic_cm)
        with mock.patch('django.contrib.admin.options.transaction.atomic', atomic_mock):
            with mock.patch('django.contrib.admin.options.router.db_for_write', return_value=alias):
                response = self.client.post(changelist_url, data)
                self.assertEqual(response.status_code, 200)
        atomic_mock.assert_called_once_with(using=alias)

@skipUnlessDBFeature('supports_transactions')
def test_atomic_context_manager_enter_exit_called(self):
    a = Swallow.objects.create(origin='Swallow A', load=4, speed=1)
    b = Swallow.objects.create(origin='Swallow B', load=2, speed=2)
    self.client.force_login(self.superuser)
    changelist_url = reverse('admin:admin_changelist_swallow_changelist')
    data = {'form-TOTAL_FORMS': '2', 'form-INITIAL_FORMS': '2', 'form-MIN_NUM_FORMS': '0', 'form-MAX_NUM_FORMS': '1000', 'form-0-uuid': str(a.pk), 'form-1-uuid': str(b.pk), 'form-0-load': '9.0', 'form-0-speed': '3.0', 'form-1-load': '5.0', 'form-1-speed': '1.0', '_save': 'Save'}
    atomic_cm = mock.MagicMock()
    enter = mock.MagicMock(return_value=None)
    exit = mock.MagicMock(return_value=None)
    atomic_cm.__enter__ = enter
    atomic_cm.__exit__ = exit
    atomic_mock = mock.MagicMock(return_value=atomic_cm)
    with mock.patch('django.contrib.admin.options.transaction.atomic', atomic_mock):
        with mock.patch('django.contrib.admin.options.router.db_for_write', return_value='other_db'):
            response = self.client.post(changelist_url, data)
            self.assertEqual(response.status_code, 200)
    atomic_mock.assert_called_once_with(using='other_db')
    self.assertTrue(enter.called)
    self.assertTrue(exit.called)

@skipUnlessDBFeature('supports_transactions')
def test_atomic_called_even_if_no_forms_have_changed(self):
    a = Swallow.objects.create(origin='Swallow A', load=4, speed=1)
    b = Swallow.objects.create(origin='Swallow B', load=2, speed=2)
    self.client.force_login(self.superuser)
    changelist_url = reverse('admin:admin_changelist_swallow_changelist')
    data = {'form-TOTAL_FORMS': '2', 'form-INITIAL_FORMS': '2', 'form-MIN_NUM_FORMS': '0', 'form-MAX_NUM_FORMS': '1000', 'form-0-uuid': str(a.pk), 'form-1-uuid': str(b.pk), 'form-0-load': str(a.load), 'form-0-speed': str(a.speed), 'form-1-load': str(b.load), 'form-1-speed': str(b.speed), '_save': 'Save'}
    atomic_cm = mock.MagicMock()
    atomic_cm.__enter__ = mock.MagicMock(return_value=None)
    atomic_cm.__exit__ = mock.MagicMock(return_value=None)
    atomic_mock = mock.MagicMock(return_value=atomic_cm)
    with mock.patch('django.contrib.admin.options.transaction.atomic', atomic_mock):
        with mock.patch('django.contrib.admin.options.router.db_for_write', return_value='other_db'):
            response = self.client.post(changelist_url, data)
            self.assertEqual(response.status_code, 200)
    atomic_mock.assert_called_once_with(using='other_db')

@skipUnlessDBFeature('supports_transactions')
def test_atomic_called_on_successful_bulk_edit(self):
    """
    Ensure transaction.atomic is called with the router.db_for_write() alias
    for a successful bulk edit.
    """
    a = Swallow.objects.create(origin='Swallow A', load=4, speed=1)
    b = Swallow.objects.create(origin='Swallow B', load=2, speed=2)
    self.client.force_login(self.superuser)
    changelist_url = reverse('admin:admin_changelist_swallow_changelist')
    data = {'form-TOTAL_FORMS': '2', 'form-INITIAL_FORMS': '2', 'form-MIN_NUM_FORMS': '0', 'form-MAX_NUM_FORMS': '1000', 'form-0-uuid': str(a.pk), 'form-1-uuid': str(b.pk), 'form-0-load': '9.0', 'form-0-speed': '3.0', 'form-1-load': '5.0', 'form-1-speed': '1.0', '_save': 'Save'}
    expected_using = 'non_default_db'

    class DummyCM:

        def __init__(self, using):
            self.using = using

        def __enter__(self):
            return None

        def __exit__(self, exc_type, exc, tb):
            return False

    def atomic_mock(*args, **kwargs):
        assert kwargs.get('using') == expected_using, 'transaction.atomic called with using=%r, expected %r' % (kwargs.get('using'), expected_using)
        return DummyCM(kwargs.get('using'))
    with mock.patch('django.contrib.admin.options.router.db_for_write', return_value=expected_using):
        with mock.patch('django.contrib.admin.options.transaction.atomic', new=atomic_mock):
            response = self.client.post(changelist_url, data)
            self.assertIn(response.status_code, (200, 302))

@skipUnlessDBFeature('supports_transactions')
def test_atomic_called_when_log_change_raises_databaseerror(self):
    """
    Ensure transaction.atomic is used when log_change raises DatabaseError.
    """
    a = Swallow.objects.create(origin='Swallow A', load=4, speed=1)
    b = Swallow.objects.create(origin='Swallow B', load=2, speed=2)
    self.client.force_login(self.superuser)
    changelist_url = reverse('admin:admin_changelist_swallow_changelist')
    data = {'form-TOTAL_FORMS': '2', 'form-INITIAL_FORMS': '2', 'form-MIN_NUM_FORMS': '0', 'form-MAX_NUM_FORMS': '1000', 'form-0-uuid': str(a.pk), 'form-1-uuid': str(b.pk), 'form-0-load': '9.0', 'form-0-speed': '3.0', 'form-1-load': '5.0', 'form-1-speed': '1.0', '_save': 'Save'}
    expected_using = 'other_db'

    class DummyCM:

        def __init__(self, using):
            self.using = using

        def __enter__(self):
            return None

        def __exit__(self, exc_type, exc, tb):
            return False

    def atomic_mock(*args, **kwargs):
        assert kwargs.get('using') == expected_using, 'transaction.atomic called with using=%r, expected %r' % (kwargs.get('using'), expected_using)
        return DummyCM(kwargs.get('using'))
    with mock.patch('django.contrib.admin.options.router.db_for_write', return_value=expected_using):
        with mock.patch('django.contrib.admin.options.transaction.atomic', new=atomic_mock):
            with mock.patch('django.contrib.admin.ModelAdmin.log_change', side_effect=DatabaseError):
                with self.assertRaises(DatabaseError):
                    self.client.post(changelist_url, data)

@skipUnlessDBFeature('supports_transactions')
def test_atomic_called_when_log_change_raises_on_second_form(self):
    """
    If log_change raises on the second changed form (side_effect list), atomic
    must still be entered with correct using kwarg.
    """
    a = Swallow.objects.create(origin='Swallow A', load=4, speed=1)
    b = Swallow.objects.create(origin='Swallow B', load=2, speed=2)
    self.client.force_login(self.superuser)
    changelist_url = reverse('admin:admin_changelist_swallow_changelist')
    data = {'form-TOTAL_FORMS': '2', 'form-INITIAL_FORMS': '2', 'form-MIN_NUM_FORMS': '0', 'form-MAX_NUM_FORMS': '1000', 'form-0-uuid': str(a.pk), 'form-1-uuid': str(b.pk), 'form-0-load': '9.0', 'form-0-speed': '3.0', 'form-1-load': '5.0', 'form-1-speed': '1.0', '_save': 'Save'}
    expected_using = 'writes_db'

    class DummyCM:

        def __init__(self, using):
            self.using = using

        def __enter__(self):
            return None

        def __exit__(self, exc_type, exc, tb):
            return False

    def atomic_mock(*args, **kwargs):
        assert kwargs.get('using') == expected_using, 'transaction.atomic called with using=%r, expected %r' % (kwargs.get('using'), expected_using)
        return DummyCM(kwargs.get('using'))
    with mock.patch('django.contrib.admin.options.router.db_for_write', return_value=expected_using):
        with mock.patch('django.contrib.admin.options.transaction.atomic', new=atomic_mock):
            with mock.patch('django.contrib.admin.ModelAdmin.log_change', side_effect=[None, DatabaseError]):
                with self.assertRaises(DatabaseError):
                    self.client.post(changelist_url, data)

@skipUnlessDBFeature('supports_transactions')
def test_atomic_called_when_save_model_raises(self):
    """
    Ensure transaction.atomic is used when save_model raises DatabaseError.
    """
    a = Swallow.objects.create(origin='Swallow A', load=4, speed=1)
    b = Swallow.objects.create(origin='Swallow B', load=2, speed=2)
    self.client.force_login(self.superuser)
    changelist_url = reverse('admin:admin_changelist_swallow_changelist')
    data = {'form-TOTAL_FORMS': '2', 'form-INITIAL_FORMS': '2', 'form-MIN_NUM_FORMS': '0', 'form-MAX_NUM_FORMS': '1000', 'form-0-uuid': str(a.pk), 'form-1-uuid': str(b.pk), 'form-0-load': '9.0', 'form-0-speed': '3.0', 'form-1-load': '5.0', 'form-1-speed': '1.0', '_save': 'Save'}
    expected_using = 'write_target'

    class DummyCM:

        def __init__(self, using):
            self.using = using

        def __enter__(self):
            return None

        def __exit__(self, exc_type, exc, tb):
            return False

    def atomic_mock(*args, **kwargs):
        assert kwargs.get('using') == expected_using, 'transaction.atomic called with using=%r, expected %r' % (kwargs.get('using'), expected_using)
        return DummyCM(kwargs.get('using'))
    with mock.patch('django.contrib.admin.options.router.db_for_write', return_value=expected_using):
        with mock.patch('django.contrib.admin.options.transaction.atomic', new=atomic_mock):
            with mock.patch('django.contrib.admin.ModelAdmin.save_model', side_effect=DatabaseError):
                with self.assertRaises(DatabaseError):
                    self.client.post(changelist_url, data)

@skipUnlessDBFeature('supports_transactions')
def test_atomic_called_when_save_related_raises(self):
    """
    Ensure transaction.atomic is used when save_related raises DatabaseError.
    """
    a = Swallow.objects.create(origin='Swallow A', load=4, speed=1)
    b = Swallow.objects.create(origin='Swallow B', load=2, speed=2)
    self.client.force_login(self.superuser)
    changelist_url = reverse('admin:admin_changelist_swallow_changelist')
    data = {'form-TOTAL_FORMS': '2', 'form-INITIAL_FORMS': '2', 'form-MIN_NUM_FORMS': '0', 'form-MAX_NUM_FORMS': '1000', 'form-0-uuid': str(a.pk), 'form-1-uuid': str(b.pk), 'form-0-load': '9.0', 'form-0-speed': '3.0', 'form-1-load': '5.0', 'form-1-speed': '1.0', '_save': 'Save'}
    expected_using = 'atomic_db'

    class DummyCM:

        def __init__(self, using):
            self.using = using

        def __enter__(self):
            return None

        def __exit__(self, exc_type, exc, tb):
            return False

    def atomic_mock(*args, **kwargs):
        assert kwargs.get('using') == expected_using, 'transaction.atomic called with using=%r, expected %r' % (kwargs.get('using'), expected_using)
        return DummyCM(kwargs.get('using'))
    with mock.patch('django.contrib.admin.options.router.db_for_write', return_value=expected_using):
        with mock.patch('django.contrib.admin.options.transaction.atomic', new=atomic_mock):
            with mock.patch('django.contrib.admin.ModelAdmin.save_related', side_effect=DatabaseError):
                with self.assertRaises(DatabaseError):
                    self.client.post(changelist_url, data)

@skipUnlessDBFeature('supports_transactions')
def test_atomic_called_when_save_form_raises(self):
    """
    Ensure transaction.atomic is used when save_form raises DatabaseError.
    """
    a = Swallow.objects.create(origin='Swallow A', load=4, speed=1)
    b = Swallow.objects.create(origin='Swallow B', load=2, speed=2)
    self.client.force_login(self.superuser)
    changelist_url = reverse('admin:admin_changelist_swallow_changelist')
    data = {'form-TOTAL_FORMS': '2', 'form-INITIAL_FORMS': '2', 'form-MIN_NUM_FORMS': '0', 'form-MAX_NUM_FORMS': '1000', 'form-0-uuid': str(a.pk), 'form-1-uuid': str(b.pk), 'form-0-load': '9.0', 'form-0-speed': '3.0', 'form-1-load': '5.0', 'form-1-speed': '1.0', '_save': 'Save'}
    expected_using = 'writes_here'

    class DummyCM:

        def __init__(self, using):
            self.using = using

        def __enter__(self):
            return None

        def __exit__(self, exc_type, exc, tb):
            return False

    def atomic_mock(*args, **kwargs):
        assert kwargs.get('using') == expected_using, 'transaction.atomic called with using=%r, expected %r' % (kwargs.get('using'), expected_using)
        return DummyCM(kwargs.get('using'))
    with mock.patch('django.contrib.admin.options.router.db_for_write', return_value=expected_using):
        with mock.patch('django.contrib.admin.options.transaction.atomic', new=atomic_mock):
            with mock.patch('django.contrib.admin.ModelAdmin.save_form', side_effect=DatabaseError):
                with self.assertRaises(DatabaseError):
                    self.client.post(changelist_url, data)

@skipUnlessDBFeature('supports_transactions')
def test_atomic_called_when_construct_change_message_raises(self):
    """
    Ensure transaction.atomic is used when construct_change_message raises an exception.
    """
    a = Swallow.objects.create(origin='Swallow A', load=4, speed=1)
    b = Swallow.objects.create(origin='Swallow B', load=2, speed=2)
    self.client.force_login(self.superuser)
    changelist_url = reverse('admin:admin_changelist_swallow_changelist')
    data = {'form-TOTAL_FORMS': '2', 'form-INITIAL_FORMS': '2', 'form-MIN_NUM_FORMS': '0', 'form-MAX_NUM_FORMS': '1000', 'form-0-uuid': str(a.pk), 'form-1-uuid': str(b.pk), 'form-0-load': '9.0', 'form-0-speed': '3.0', 'form-1-load': '5.0', 'form-1-speed': '1.0', '_save': 'Save'}
    expected_using = 'target_db'

    class DummyCM:

        def __init__(self, using):
            self.using = using

        def __enter__(self):
            return None

        def __exit__(self, exc_type, exc, tb):
            return False

    def atomic_mock(*args, **kwargs):
        assert kwargs.get('using') == expected_using, 'transaction.atomic called with using=%r, expected %r' % (kwargs.get('using'), expected_using)
        return DummyCM(kwargs.get('using'))
    with mock.patch('django.contrib.admin.options.router.db_for_write', return_value=expected_using):
        with mock.patch('django.contrib.admin.options.transaction.atomic', new=atomic_mock):
            with mock.patch('django.contrib.admin.options.construct_change_message', side_effect=DatabaseError):
                with self.assertRaises(DatabaseError):
                    self.client.post(changelist_url, data)

@skipUnlessDBFeature('supports_transactions')
def test_atomic_called_when_only_one_form_changed(self):
    """
    Even if only one form in the formset has changed, atomic must be used.
    """
    a = Swallow.objects.create(origin='Swallow A', load=4, speed=1)
    b = Swallow.objects.create(origin='Swallow B', load=2, speed=2)
    self.client.force_login(self.superuser)
    changelist_url = reverse('admin:admin_changelist_swallow_changelist')
    data = {'form-TOTAL_FORMS': '2', 'form-INITIAL_FORMS': '2', 'form-MIN_NUM_FORMS': '0', 'form-MAX_NUM_FORMS': '1000', 'form-0-uuid': str(a.pk), 'form-1-uuid': str(b.pk), 'form-0-load': '9.0', 'form-0-speed': '3.0', 'form-1-load': str(b.load), 'form-1-speed': str(b.speed), '_save': 'Save'}
    expected_using = 'writes_only'

    class DummyCM:

        def __init__(self, using):
            self.using = using

        def __enter__(self):
            return None

        def __exit__(self, exc_type, exc, tb):
            return False

    def atomic_mock(*args, **kwargs):
        assert kwargs.get('using') == expected_using, 'transaction.atomic called with using=%r, expected %r' % (kwargs.get('using'), expected_using)
        return DummyCM(kwargs.get('using'))
    with mock.patch('django.contrib.admin.options.router.db_for_write', return_value=expected_using):
        with mock.patch('django.contrib.admin.options.transaction.atomic', new=atomic_mock):
            response = self.client.post(changelist_url, data)
            self.assertIn(response.status_code, (200, 302))

@skipUnlessDBFeature('supports_transactions')
def test_atomic_called_when_no_form_has_changed(self):
    """
    If none of the forms have changed, the code still enters the atomic
    context (formset is valid) and atomic must be called with the correct using.
    """
    a = Swallow.objects.create(origin='Swallow A', load=4, speed=1)
    b = Swallow.objects.create(origin='Swallow B', load=2, speed=2)
    self.client.force_login(self.superuser)
    changelist_url = reverse('admin:admin_changelist_swallow_changelist')
    data = {'form-TOTAL_FORMS': '2', 'form-INITIAL_FORMS': '2', 'form-MIN_NUM_FORMS': '0', 'form-MAX_NUM_FORMS': '1000', 'form-0-uuid': str(a.pk), 'form-1-uuid': str(b.pk), 'form-0-load': str(a.load), 'form-0-speed': str(a.speed), 'form-1-load': str(b.load), 'form-1-speed': str(b.speed), '_save': 'Save'}
    expected_using = 'writes_none'

    class DummyCM:

        def __init__(self, using):
            self.using = using

        def __enter__(self):
            return None

        def __exit__(self, exc_type, exc, tb):
            return False

    def atomic_mock(*args, **kwargs):
        assert kwargs.get('using') == expected_using, 'transaction.atomic called with using=%r, expected %r' % (kwargs.get('using'), expected_using)
        return DummyCM(kwargs.get('using'))
    with mock.patch('django.contrib.admin.options.router.db_for_write', return_value=expected_using):
        with mock.patch('django.contrib.admin.options.transaction.atomic', new=atomic_mock):
            response = self.client.post(changelist_url, data)
            self.assertIn(response.status_code, (200, 302))

from unittest import mock
from django.db import DatabaseError
from django.test import skipUnlessDBFeature
from django.urls import reverse

@skipUnlessDBFeature('supports_transactions')
def test_list_editable_atomic_called_with_router_db_for_write_single_change(self):
    """
    Ensure transaction.atomic is called with using=router.db_for_write(self.model)
    when a single list_editable form is saved.
    """
    a = Swallow.objects.create(origin='Swallow A', load=4, speed=1)
    self.client.force_login(self.superuser)
    changelist_url = reverse('admin:admin_changelist_swallow_changelist')
    data = {'form-TOTAL_FORMS': '1', 'form-INITIAL_FORMS': '1', 'form-MIN_NUM_FORMS': '0', 'form-MAX_NUM_FORMS': '1000', 'form-0-uuid': str(a.pk), 'form-0-load': '7.0', 'form-0-speed': '3.0', '_save': 'Save'}
    recorded = []

    def fake_atomic(*args, **kwargs):
        recorded.append(kwargs)

        class CM:

            def __enter__(self):
                return None

            def __exit__(self, exc_type, exc, tb):
                return False
        return CM()
    with mock.patch('django.db.router.db_for_write', return_value='other_db'):
        with mock.patch('django.db.transaction.atomic', new=fake_atomic):
            resp = self.client.post(changelist_url, data)
    self.assertEqual(resp.status_code, 200)
    self.assertTrue(recorded, 'transaction.atomic was not called')
    self.assertEqual(recorded[0].get('using'), 'other_db')

@skipUnlessDBFeature('supports_transactions')
def test_list_editable_atomic_called_with_router_db_for_write_multiple_changes(self):
    """
    Ensure transaction.atomic is called with using=router.db_for_write(self.model)
    when multiple list_editable forms are saved.
    """
    a = Swallow.objects.create(origin='Swallow A', load=4, speed=1)
    b = Swallow.objects.create(origin='Swallow B', load=2, speed=2)
    c = Swallow.objects.create(origin='Swallow C', load=5, speed=5)
    self.client.force_login(self.superuser)
    changelist_url = reverse('admin:admin_changelist_swallow_changelist')
    data = {'form-TOTAL_FORMS': '3', 'form-INITIAL_FORMS': '3', 'form-MIN_NUM_FORMS': '0', 'form-MAX_NUM_FORMS': '1000', 'form-0-uuid': str(a.pk), 'form-0-load': '9.0', 'form-0-speed': '9.0', 'form-1-uuid': str(b.pk), 'form-1-load': '5.0', 'form-1-speed': '5.0', 'form-2-uuid': str(c.pk), 'form-2-load': '5.0', 'form-2-speed': '4.0', '_save': 'Save'}
    recorded = []

    def fake_atomic(*args, **kwargs):
        recorded.append(kwargs)

        class CM:

            def __enter__(self):
                return None

            def __exit__(self, exc_type, exc, tb):
                return False
        return CM()
    with mock.patch('django.db.router.db_for_write', return_value='custom_db'):
        with mock.patch('django.db.transaction.atomic', new=fake_atomic):
            resp = self.client.post(changelist_url, data)
    self.assertEqual(resp.status_code, 200)
    self.assertTrue(recorded)
    self.assertEqual(recorded[0].get('using'), 'custom_db')

@skipUnlessDBFeature('supports_transactions')
def test_list_editable_atomic_called_with_router_db_for_write_when_router_returns_none(self):
    """
    If router.db_for_write returns None, transaction.atomic should be called
    with using=None (explicit kw) by the fixed implementation.
    """
    a = Swallow.objects.create(origin='Swallow A', load=4, speed=1)
    self.client.force_login(self.superuser)
    changelist_url = reverse('admin:admin_changelist_swallow_changelist')
    data = {'form-TOTAL_FORMS': '1', 'form-INITIAL_FORMS': '1', 'form-MIN_NUM_FORMS': '0', 'form-MAX_NUM_FORMS': '1000', 'form-0-uuid': str(a.pk), 'form-0-load': '8.0', 'form-0-speed': '2.0', '_save': 'Save'}
    recorded = []

    def fake_atomic(*args, **kwargs):
        recorded.append(kwargs)

        class CM:

            def __enter__(self):
                return None

            def __exit__(self, exc_type, exc, tb):
                return False
        return CM()
    with mock.patch('django.db.router.db_for_write', return_value=None):
        with mock.patch('django.db.transaction.atomic', new=fake_atomic):
            resp = self.client.post(changelist_url, data)
    self.assertEqual(resp.status_code, 200)
    self.assertTrue(recorded)
    self.assertIn('using', recorded[0])
    self.assertIsNone(recorded[0]['using'])

@skipUnlessDBFeature('supports_transactions')
def test_list_editable_atomic_called_with_router_db_for_write_when_router_returns_default(self):
    """
    If router.db_for_write returns 'default', transaction.atomic should be
    called with using='default'.
    """
    a = Swallow.objects.create(origin='Swallow A', load=4, speed=1)
    self.client.force_login(self.superuser)
    changelist_url = reverse('admin:admin_changelist_swallow_changelist')
    data = {'form-TOTAL_FORMS': '1', 'form-INITIAL_FORMS': '1', 'form-MIN_NUM_FORMS': '0', 'form-MAX_NUM_FORMS': '1000', 'form-0-uuid': str(a.pk), 'form-0-load': '6.0', 'form-0-speed': '2.5', '_save': 'Save'}
    recorded = []

    def fake_atomic(*args, **kwargs):
        recorded.append(kwargs)

        class CM:

            def __enter__(self):
                return None

            def __exit__(self, exc_type, exc, tb):
                return False
        return CM()
    with mock.patch('django.db.router.db_for_write', return_value='default'):
        with mock.patch('django.db.transaction.atomic', new=fake_atomic):
            resp = self.client.post(changelist_url, data)
    self.assertEqual(resp.status_code, 200)
    self.assertTrue(recorded)
    self.assertEqual(recorded[0].get('using'), 'default')

@skipUnlessDBFeature('supports_transactions')
def test_list_editable_atomic_called_even_when_some_forms_unchanged(self):
    """
    Ensure atomic is still invoked even if only a subset of submitted forms
    have changes.
    """
    a = Swallow.objects.create(origin='Swallow A', load=4, speed=1)
    b = Swallow.objects.create(origin='Swallow B', load=2, speed=2)
    self.client.force_login(self.superuser)
    changelist_url = reverse('admin:admin_changelist_swallow_changelist')
    data = {'form-TOTAL_FORMS': '2', 'form-INITIAL_FORMS': '2', 'form-MIN_NUM_FORMS': '0', 'form-MAX_NUM_FORMS': '1000', 'form-0-uuid': str(a.pk), 'form-0-load': '11.0', 'form-0-speed': '4.0', 'form-1-uuid': str(b.pk), 'form-1-load': '2.0', 'form-1-speed': '2.0', '_save': 'Save'}
    recorded = []

    def fake_atomic(*args, **kwargs):
        recorded.append(kwargs)

        class CM:

            def __enter__(self):
                return None

            def __exit__(self, exc_type, exc, tb):
                return False
        return CM()
    with mock.patch('django.db.router.db_for_write', return_value='other_one'):
        with mock.patch('django.db.transaction.atomic', new=fake_atomic):
            resp = self.client.post(changelist_url, data)
    self.assertEqual(resp.status_code, 200)
    self.assertTrue(recorded)
    self.assertEqual(recorded[0].get('using'), 'other_one')

@skipUnlessDBFeature('supports_transactions')
def test_list_editable_atomic_called_when_log_change_raises(self):
    """
    Even when an exception (DatabaseError) occurs during log_change, the
    transaction.atomic context manager should have been entered with the
    correct 'using' kwarg.
    """
    a = Swallow.objects.create(origin='Swallow A', load=4, speed=1)
    b = Swallow.objects.create(origin='Swallow B', load=2, speed=2)
    self.client.force_login(self.superuser)
    changelist_url = reverse('admin:admin_changelist_swallow_changelist')
    data = {'form-TOTAL_FORMS': '2', 'form-INITIAL_FORMS': '2', 'form-MIN_NUM_FORMS': '0', 'form-MAX_NUM_FORMS': '1000', 'form-0-uuid': str(a.pk), 'form-0-load': '9.0', 'form-0-speed': '3.0', 'form-1-uuid': str(b.pk), 'form-1-load': '5.0', 'form-1-speed': '5.0', '_save': 'Save'}
    recorded = []

    def fake_atomic(*args, **kwargs):
        recorded.append(kwargs)

        class CM:

            def __enter__(self):
                return None

            def __exit__(self, exc_type, exc, tb):
                return False
        return CM()
    with mock.patch('django.db.router.db_for_write', return_value='db_for_write_here'):
        with mock.patch('django.db.transaction.atomic', new=fake_atomic):
            with mock.patch('django.contrib.admin.ModelAdmin.log_change', side_effect=DatabaseError):
                with self.assertRaises(DatabaseError):
                    self.client.post(changelist_url, data)
    self.assertTrue(recorded)
    self.assertEqual(recorded[0].get('using'), 'db_for_write_here')

@skipUnlessDBFeature('supports_transactions')
def test_list_editable_atomic_called_for_multiple_saved_forms_ordering(self):
    """
    Ensure atomic is used when several forms are saved and ordering/pk handling
    is involved (replicating scenario similar to multiuser edit).
    """
    a = Swallow.objects.create(origin='A', load=4, speed=1)
    b = Swallow.objects.create(origin='B', load=2, speed=2)
    c = Swallow.objects.create(origin='C', load=5, speed=5)
    d = Swallow.objects.create(origin='D', load=9, speed=9)
    self.client.force_login(self.superuser)
    changelist_url = reverse('admin:admin_changelist_swallow_changelist')
    data = {'form-TOTAL_FORMS': '3', 'form-INITIAL_FORMS': '3', 'form-MIN_NUM_FORMS': '0', 'form-MAX_NUM_FORMS': '1000', 'form-0-uuid': str(d.pk), 'form-1-uuid': str(c.pk), 'form-2-uuid': str(a.pk), 'form-0-load': '9.0', 'form-0-speed': '9.0', 'form-1-load': '5.0', 'form-1-speed': '5.0', 'form-2-load': '5.0', 'form-2-speed': '4.0', '_save': 'Save'}
    recorded = []

    def fake_atomic(*args, **kwargs):
        recorded.append(kwargs)

        class CM:

            def __enter__(self):
                return None

            def __exit__(self, exc_type, exc, tb):
                return False
        return CM()
    with mock.patch('django.db.router.db_for_write', return_value='ordering_db'):
        with mock.patch('django.db.transaction.atomic', new=fake_atomic):
            resp = self.client.post(changelist_url, data, follow=True, extra={'o': '-2'})
    self.assertEqual(resp.status_code, 200)
    self.assertTrue(recorded)
    self.assertEqual(recorded[0].get('using'), 'ordering_db')

@skipUnlessDBFeature('supports_transactions')
def test_list_editable_atomic_called_when_prefix_contains_regex_chars(self):
    """
    If the form prefix contains regex special characters (e.g. 'form$'),
    the changelist form processing still uses transaction.atomic(using=...).
    """
    a = Swallow.objects.create(origin='Swallow A', load=4, speed=1)
    b = Swallow.objects.create(origin='Swallow B', load=2, speed=2)
    self.client.force_login(self.superuser)
    changelist_url = reverse('admin:admin_changelist_swallow_changelist')
    data = {'form$-TOTAL_FORMS': '2', 'form$-INITIAL_FORMS': '2', 'form$-MIN_NUM_FORMS': '0', 'form$-MAX_NUM_FORMS': '1000', 'form$-0-uuid': str(a.pk), 'form$-0-load': '10', 'form$-0-speed': '3', 'form$-1-uuid': str(b.pk), 'form$-1-load': '5', 'form$-1-speed': '5', '_save': 'Save'}
    recorded = []

    def fake_atomic(*args, **kwargs):
        recorded.append(kwargs)

        class CM:

            def __enter__(self):
                return None

            def __exit__(self, exc_type, exc, tb):
                return False
        return CM()
    with mock.patch('django.db.router.db_for_write', return_value='regex_db'):
        with mock.patch('django.db.transaction.atomic', new=fake_atomic):
            resp = self.client.post(changelist_url, data)
    self.assertEqual(resp.status_code, 200)
    self.assertTrue(recorded)
    self.assertEqual(recorded[0].get('using'), 'regex_db')

@skipUnlessDBFeature('supports_transactions')
def test_list_editable_atomic_called_when_select_across_flag_present(self):
    """
    Ensure transaction.atomic is used when select_across option may be present.
    This is exercising the standard list_editable save path with a normal payload.
    """
    a = Swallow.objects.create(origin='Swallow A', load=4, speed=1)
    b = Swallow.objects.create(origin='Swallow B', load=2, speed=2)
    self.client.force_login(self.superuser)
    changelist_url = reverse('admin:admin_changelist_swallow_changelist')
    data = {'form-TOTAL_FORMS': '2', 'form-INITIAL_FORMS': '2', 'form-MIN_NUM_FORMS': '0', 'form-MAX_NUM_FORMS': '1000', 'form-0-uuid': str(a.pk), 'form-0-load': '10', 'form-0-speed': '3', 'form-1-uuid': str(b.pk), 'form-1-load': '5', 'form-1-speed': '5', 'select_across': '1', '_save': 'Save'}
    recorded = []

    def fake_atomic(*args, **kwargs):
        recorded.append(kwargs)

        class CM:

            def __enter__(self):
                return None

            def __exit__(self, exc_type, exc, tb):
                return False
        return CM()
    with mock.patch('django.db.router.db_for_write', return_value='select_across_db'):
        with mock.patch('django.db.transaction.atomic', new=fake_atomic):
            resp = self.client.post(changelist_url, data)
    self.assertEqual(resp.status_code, 200)
    self.assertTrue(recorded)
    self.assertEqual(recorded[0].get('using'), 'select_across_db')