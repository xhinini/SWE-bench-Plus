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