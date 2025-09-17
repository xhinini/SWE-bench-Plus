from django import forms
from django.contrib import admin
from django.test import SimpleTestCase
from django.db.models import ForeignKey
from .models import Inventory, Event

class ForeignKeyEmptyLabelPreservationTests(SimpleTestCase):

    def test_formfield_overrides_empty_string_preserved(self):

        class MyAdmin(admin.ModelAdmin):
            radio_fields = {'parent': admin.VERTICAL}
            formfield_overrides = {ForeignKey: {'empty_label': ''}}
        ma = MyAdmin(Inventory, admin.site)
        ff = ma.formfield_for_dbfield(Inventory._meta.get_field('parent'), request=None)
        self.assertEqual(ff.empty_label, '')

    def test_formfield_overrides_none_preserved(self):

        class MyAdmin(admin.ModelAdmin):
            radio_fields = {'parent': admin.VERTICAL}
            formfield_overrides = {ForeignKey: {'empty_label': None}}
        ma = MyAdmin(Inventory, admin.site)
        ff = ma.formfield_for_dbfield(Inventory._meta.get_field('parent'), request=None)
        self.assertIsNone(ff.empty_label)

    def test_formfield_overrides_false_preserved(self):

        class MyAdmin(admin.ModelAdmin):
            radio_fields = {'parent': admin.VERTICAL}
            formfield_overrides = {ForeignKey: {'empty_label': False}}
        ma = MyAdmin(Inventory, admin.site)
        ff = ma.formfield_for_dbfield(Inventory._meta.get_field('parent'), request=None)
        self.assertIs(ff.empty_label, False)

    def test_formfield_overrides_zero_preserved(self):

        class MyAdmin(admin.ModelAdmin):
            radio_fields = {'parent': admin.VERTICAL}
            formfield_overrides = {ForeignKey: {'empty_label': 0}}
        ma = MyAdmin(Inventory, admin.site)
        ff = ma.formfield_for_dbfield(Inventory._meta.get_field('parent'), request=None)
        self.assertEqual(ff.empty_label, 0)

    def test_formfield_for_foreignkey_kwargs_empty_string_preserved(self):

        class MyAdmin(admin.ModelAdmin):
            radio_fields = {'parent': admin.VERTICAL}
        ma = MyAdmin(Inventory, admin.site)
        ff = ma.formfield_for_foreignkey(Inventory._meta.get_field('parent'), request=None, empty_label='')
        self.assertEqual(ff.empty_label, '')

    def test_formfield_for_foreignkey_kwargs_none_preserved(self):

        class MyAdmin(admin.ModelAdmin):
            radio_fields = {'parent': admin.VERTICAL}
        ma = MyAdmin(Inventory, admin.site)
        ff = ma.formfield_for_foreignkey(Inventory._meta.get_field('parent'), request=None, empty_label=None)
        self.assertIsNone(ff.empty_label)

    def test_formfield_for_foreignkey_kwargs_false_preserved(self):

        class MyAdmin(admin.ModelAdmin):
            radio_fields = {'parent': admin.VERTICAL}
        ma = MyAdmin(Inventory, admin.site)
        ff = ma.formfield_for_foreignkey(Inventory._meta.get_field('parent'), request=None, empty_label=False)
        self.assertIs(ff.empty_label, False)

    def test_formfield_for_foreignkey_kwargs_zero_preserved(self):

        class MyAdmin(admin.ModelAdmin):
            radio_fields = {'parent': admin.VERTICAL}
        ma = MyAdmin(Inventory, admin.site)
        ff = ma.formfield_for_foreignkey(Inventory._meta.get_field('parent'), request=None, empty_label=0)
        self.assertEqual(ff.empty_label, 0)

    def test_formfield_for_dbfield_kwargs_empty_string_preserved(self):

        class MyAdmin(admin.ModelAdmin):
            radio_fields = {'parent': admin.VERTICAL}
        ma = MyAdmin(Inventory, admin.site)
        ff = ma.formfield_for_dbfield(Inventory._meta.get_field('parent'), request=None, empty_label='')
        self.assertEqual(ff.empty_label, '')

from django import forms
from django.contrib import admin
from django.db.models import ForeignKey
from django.test import SimpleTestCase
from .models import Inventory
from django import forms
from django.contrib import admin
from django.db.models import ForeignKey
from django.test import SimpleTestCase
from .models import Inventory

class RadioFieldsEmptyLabelRegressionTests(SimpleTestCase):
    """
    Regression tests for preserving falsy empty_label overrides for radio
    ForeignKey widgets (see formfield_for_foreignkey handling of radio_fields).
    """

    def _get_fk_field(self):
        return Inventory._meta.get_field('parent')

    def test_empty_string_in_formfield_overrides_is_preserved(self):
        self._assert_override_kept_via_formfield_overrides('')

    def test_empty_string_passed_as_kwarg_is_preserved(self):
        self._assert_override_kept_via_kwargs('')

    def test_none_in_formfield_overrides_is_preserved(self):
        self._assert_override_kept_via_formfield_overrides(None)

    def test_none_passed_as_kwarg_is_preserved(self):
        self._assert_override_kept_via_kwargs(None)

    def test_false_in_formfield_overrides_is_preserved(self):
        self._assert_override_kept_via_formfield_overrides(False)

    def test_false_passed_as_kwarg_is_preserved(self):
        self._assert_override_kept_via_kwargs(False)

    def test_zero_in_formfield_overrides_is_preserved(self):
        self._assert_override_kept_via_formfield_overrides(0)

    def test_zero_passed_as_kwarg_is_preserved(self):
        self._assert_override_kept_via_kwargs(0)

    def test_empty_list_in_formfield_overrides_is_preserved(self):
        self._assert_override_kept_via_formfield_overrides([])

    def test_empty_list_passed_as_kwarg_is_preserved(self):
        self._assert_override_kept_via_kwargs([])