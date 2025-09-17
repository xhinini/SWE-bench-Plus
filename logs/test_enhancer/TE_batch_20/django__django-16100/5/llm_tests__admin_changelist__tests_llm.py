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