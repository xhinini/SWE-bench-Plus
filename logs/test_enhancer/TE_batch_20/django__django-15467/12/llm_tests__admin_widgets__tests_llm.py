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

from django.contrib import admin
from django.db.models import ForeignKey
from django.utils.translation import gettext as _
from django.contrib import admin
from django.db.models import ForeignKey
from django.test import SimpleTestCase
from django.utils.translation import gettext as _
from admin_widgets.models import Inventory, Event

class AdminRadioFieldEmptyLabelTests(SimpleTestCase):
    """
    Regression tests for formfield_for_foreignkey radio_fields empty_label handling.
    """

    def test_preserve_empty_string_override_vertical(self):

        class MyModelAdmin(admin.ModelAdmin):
            radio_fields = {'parent': admin.VERTICAL}
            formfield_overrides = {ForeignKey: {'empty_label': ''}}
        ma = MyModelAdmin(Inventory, admin.site)
        ff = ma.formfield_for_dbfield(Inventory._meta.get_field('parent'), request=None)
        self.assertEqual(ff.empty_label, '')

    def test_preserve_empty_string_override_horizontal(self):

        class MyModelAdmin(admin.ModelAdmin):
            radio_fields = {'parent': admin.HORIZONTAL}
            formfield_overrides = {ForeignKey: {'empty_label': ''}}
        ma = MyModelAdmin(Inventory, admin.site)
        ff = ma.formfield_for_dbfield(Inventory._meta.get_field('parent'), request=None)
        self.assertEqual(ff.empty_label, '')

    def test_preserve_none_override_vertical(self):

        class MyModelAdmin(admin.ModelAdmin):
            radio_fields = {'parent': admin.VERTICAL}
            formfield_overrides = {ForeignKey: {'empty_label': None}}
        ma = MyModelAdmin(Inventory, admin.site)
        ff = ma.formfield_for_dbfield(Inventory._meta.get_field('parent'), request=None)
        self.assertIs(ff.empty_label, None)

    def test_preserve_none_override_horizontal(self):

        class MyModelAdmin(admin.ModelAdmin):
            radio_fields = {'parent': admin.HORIZONTAL}
            formfield_overrides = {ForeignKey: {'empty_label': None}}
        ma = MyModelAdmin(Inventory, admin.site)
        ff = ma.formfield_for_dbfield(Inventory._meta.get_field('parent'), request=None)
        self.assertIs(ff.empty_label, None)

from django import forms
from django.contrib import admin
from django import forms
from django.contrib import admin
from django.test import SimpleTestCase
from .models import Event, Inventory
from django.contrib.admin import widgets

class RadioForeignKeyEmptyLabelTests(SimpleTestCase):
    """
    Regression tests for formfield_for_foreignkey handling of empty_label when
    radio_fields is used. Ensures that falsy but explicit empty_label values
    (like '', None or 0) provided through formfield_overrides or kwargs are
    respected.
    """

    def test_direct_kw_empty_label_empty_string(self):

        class MyModelAdmin(admin.ModelAdmin):
            radio_fields = {'parent': admin.VERTICAL}
        ma = MyModelAdmin(Inventory, admin.site)
        ff = ma.formfield_for_dbfield(Inventory._meta.get_field('parent'), request=None, empty_label='')
        self.assertEqual(ff.empty_label, '')

    def test_direct_kw_empty_label_none(self):

        class MyModelAdmin(admin.ModelAdmin):
            radio_fields = {'parent': admin.VERTICAL}
        ma = MyModelAdmin(Inventory, admin.site)
        ff = ma.formfield_for_dbfield(Inventory._meta.get_field('parent'), request=None, empty_label=None)
        self.assertIsNone(ff.empty_label)

    def test_direct_kw_empty_label_zero(self):

        class MyModelAdmin(admin.ModelAdmin):
            radio_fields = {'parent': admin.VERTICAL}
        ma = MyModelAdmin(Inventory, admin.site)
        ff = ma.formfield_for_dbfield(Inventory._meta.get_field('parent'), request=None, empty_label=0)
        self.assertEqual(ff.empty_label, 0)

from django.utils.translation import gettext as _
from django.test import SimpleTestCase
from django.utils.translation import gettext as _
from django import forms
from django.contrib import admin
from django.contrib.admin import widgets
from .models import Inventory
from django.db.models import ForeignKey

class RadioFieldsEmptyLabelTests(SimpleTestCase):

    def test_preserve_empty_string_from_formfield_overrides_vertical(self):

        class MyModelAdmin(admin.ModelAdmin):
            radio_fields = {'parent': admin.VERTICAL}
            formfield_overrides = {ForeignKey: {'empty_label': ''}}
        ma = MyModelAdmin(Inventory, admin.site)
        ff = ma.formfield_for_dbfield(Inventory._meta.get_field('parent'), request=None)
        self.assertEqual(ff.empty_label, '')

    def test_preserve_none_from_formfield_overrides_vertical(self):

        class MyModelAdmin(admin.ModelAdmin):
            radio_fields = {'parent': admin.VERTICAL}
            formfield_overrides = {ForeignKey: {'empty_label': None}}
        ma = MyModelAdmin(Inventory, admin.site)
        ff = ma.formfield_for_dbfield(Inventory._meta.get_field('parent'), request=None)
        self.assertIsNone(ff.empty_label)

    def test_preserve_empty_string_from_kwargs_vertical(self):

        class MyModelAdmin(admin.ModelAdmin):
            radio_fields = {'parent': admin.VERTICAL}
        ma = MyModelAdmin(Inventory, admin.site)
        ff = ma.formfield_for_foreignkey(Inventory._meta.get_field('parent'), request=None, empty_label='')
        self.assertEqual(ff.empty_label, '')

    def test_preserve_none_from_kwargs_vertical(self):

        class MyModelAdmin(admin.ModelAdmin):
            radio_fields = {'parent': admin.VERTICAL}
        ma = MyModelAdmin(Inventory, admin.site)
        ff = ma.formfield_for_foreignkey(Inventory._meta.get_field('parent'), request=None, empty_label=None)
        self.assertIsNone(ff.empty_label)

    def test_preserve_empty_string_from_formfield_overrides_horizontal(self):

        class MyModelAdmin(admin.ModelAdmin):
            radio_fields = {'parent': admin.HORIZONTAL}
            formfield_overrides = {ForeignKey: {'empty_label': ''}}
        ma = MyModelAdmin(Inventory, admin.site)
        ff = ma.formfield_for_dbfield(Inventory._meta.get_field('parent'), request=None)
        self.assertEqual(ff.empty_label, '')

    def test_preserve_none_from_formfield_overrides_horizontal(self):

        class MyModelAdmin(admin.ModelAdmin):
            radio_fields = {'parent': admin.HORIZONTAL}
            formfield_overrides = {ForeignKey: {'empty_label': None}}
        ma = MyModelAdmin(Inventory, admin.site)
        ff = ma.formfield_for_dbfield(Inventory._meta.get_field('parent'), request=None)
        self.assertIsNone(ff.empty_label)

from django import forms
from django.contrib import admin
from django.test import SimpleTestCase
from django.db.models import ForeignKey
from .models import Inventory, Event
from django.contrib.admin import widgets

class EmptyLabelRegressionTests(SimpleTestCase):

    def test_preserve_empty_string_from_formfield_overrides_vertical(self):

        class MyModelAdmin(admin.ModelAdmin):
            radio_fields = {'parent': admin.VERTICAL}
            formfield_overrides = {ForeignKey: {'empty_label': ''}}
        ma = MyModelAdmin(Inventory, admin.site)
        ff = ma.formfield_for_dbfield(Inventory._meta.get_field('parent'), request=None)
        self.assertEqual(ff.empty_label, '')

    def test_preserve_none_from_formfield_overrides_vertical(self):

        class MyModelAdmin(admin.ModelAdmin):
            radio_fields = {'parent': admin.VERTICAL}
            formfield_overrides = {ForeignKey: {'empty_label': None}}
        ma = MyModelAdmin(Inventory, admin.site)
        ff = ma.formfield_for_dbfield(Inventory._meta.get_field('parent'), request=None)
        self.assertIsNone(ff.empty_label)

    def test_preserve_false_from_formfield_overrides_vertical(self):

        class MyModelAdmin(admin.ModelAdmin):
            radio_fields = {'parent': admin.VERTICAL}
            formfield_overrides = {ForeignKey: {'empty_label': False}}
        ma = MyModelAdmin(Inventory, admin.site)
        ff = ma.formfield_for_dbfield(Inventory._meta.get_field('parent'), request=None)
        self.assertIs(ff.empty_label, False)

    def test_preserve_empty_string_from_formfield_overrides_horizontal(self):

        class MyModelAdmin(admin.ModelAdmin):
            radio_fields = {'parent': admin.HORIZONTAL}
            formfield_overrides = {ForeignKey: {'empty_label': ''}}
        ma = MyModelAdmin(Inventory, admin.site)
        ff = ma.formfield_for_dbfield(Inventory._meta.get_field('parent'), request=None)
        self.assertEqual(ff.empty_label, '')

    def test_preserve_none_from_formfield_overrides_horizontal(self):

        class MyModelAdmin(admin.ModelAdmin):
            radio_fields = {'parent': admin.HORIZONTAL}
            formfield_overrides = {ForeignKey: {'empty_label': None}}
        ma = MyModelAdmin(Inventory, admin.site)
        ff = ma.formfield_for_dbfield(Inventory._meta.get_field('parent'), request=None)
        self.assertIsNone(ff.empty_label)

    def test_preserve_empty_string_passed_as_kwarg_vertical(self):

        class MyModelAdmin(admin.ModelAdmin):
            radio_fields = {'parent': admin.VERTICAL}
        ma = MyModelAdmin(Inventory, admin.site)
        ff = ma.formfield_for_dbfield(Inventory._meta.get_field('parent'), request=None, empty_label='')
        self.assertEqual(ff.empty_label, '')

    def test_preserve_none_passed_as_kwarg_vertical(self):

        class MyModelAdmin(admin.ModelAdmin):
            radio_fields = {'parent': admin.VERTICAL}
        ma = MyModelAdmin(Inventory, admin.site)
        ff = ma.formfield_for_dbfield(Inventory._meta.get_field('parent'), request=None, empty_label=None)
        self.assertIsNone(ff.empty_label)

from django.test import SimpleTestCase
from django import forms
from django.contrib import admin
from django.db.models import ForeignKey
from .models import Inventory, Event

class AdminForeignKeyEmptyLabelTests(SimpleTestCase):
    """
    Regression tests for preservation of explicit empty_label values when
    rendering ForeignKey fields as radio fields in the admin.
    """

    def test_preserves_empty_string_from_formfield_overrides_vertical(self):

        class MyModelAdmin(admin.ModelAdmin):
            radio_fields = {'parent': admin.VERTICAL}
            formfield_overrides = {ForeignKey: {'empty_label': ''}}
        ma = MyModelAdmin(Inventory, admin.site)
        ff = ma.formfield_for_dbfield(Inventory._meta.get_field('parent'), request=None)
        self.assertEqual(ff.empty_label, '')

    def test_preserves_none_from_formfield_overrides_vertical(self):

        class MyModelAdmin(admin.ModelAdmin):
            radio_fields = {'parent': admin.VERTICAL}
            formfield_overrides = {ForeignKey: {'empty_label': None}}
        ma = MyModelAdmin(Inventory, admin.site)
        ff = ma.formfield_for_dbfield(Inventory._meta.get_field('parent'), request=None)
        self.assertIs(ff.empty_label, None)

    def test_preserves_false_from_formfield_overrides_vertical(self):

        class MyModelAdmin(admin.ModelAdmin):
            radio_fields = {'parent': admin.VERTICAL}
            formfield_overrides = {ForeignKey: {'empty_label': False}}
        ma = MyModelAdmin(Inventory, admin.site)
        ff = ma.formfield_for_dbfield(Inventory._meta.get_field('parent'), request=None)
        self.assertIs(ff.empty_label, False)

    def test_preserves_empty_string_passed_as_kwarg_vertical(self):

        class MyModelAdmin(admin.ModelAdmin):
            radio_fields = {'parent': admin.VERTICAL}
        ma = MyModelAdmin(Inventory, admin.site)
        ff = ma.formfield_for_dbfield(Inventory._meta.get_field('parent'), request=None, empty_label='')
        self.assertEqual(ff.empty_label, '')

    def test_preserves_none_passed_as_kwarg_vertical(self):

        class MyModelAdmin(admin.ModelAdmin):
            radio_fields = {'parent': admin.VERTICAL}
        ma = MyModelAdmin(Inventory, admin.site)
        ff = ma.formfield_for_dbfield(Inventory._meta.get_field('parent'), request=None, empty_label=None)
        self.assertIs(ff.empty_label, None)

    def test_preserves_empty_string_from_formfield_overrides_horizontal(self):

        class MyModelAdmin(admin.ModelAdmin):
            radio_fields = {'parent': admin.HORIZONTAL}
            formfield_overrides = {ForeignKey: {'empty_label': ''}}
        ma = MyModelAdmin(Inventory, admin.site)
        ff = ma.formfield_for_dbfield(Inventory._meta.get_field('parent'), request=None)
        self.assertEqual(ff.empty_label, '')

    def test_preserves_empty_string_passed_as_kwarg_horizontal(self):

        class MyModelAdmin(admin.ModelAdmin):
            radio_fields = {'parent': admin.HORIZONTAL}
        ma = MyModelAdmin(Inventory, admin.site)
        ff = ma.formfield_for_dbfield(Inventory._meta.get_field('parent'), request=None, empty_label='')
        self.assertEqual(ff.empty_label, '')