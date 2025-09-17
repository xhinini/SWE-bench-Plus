from django import forms
from django.contrib import admin
from django.contrib.admin import widgets as admin_widgets
from django import forms
from django.contrib import admin
from django.test import SimpleTestCase
from django.contrib.admin import widgets
from .models import Band
from django.contrib.admin import widgets as admin_widgets

def _unwrap_widget(field):
    """
    Helper to get the underlying widget (unwrapping RelatedFieldWidgetWrapper
    if present).
    """
    w = field.widget
    if isinstance(w, admin_widgets.RelatedFieldWidgetWrapper):
        return w.widget
    return w

from django import forms
from django.contrib import admin
from django.contrib.admin import widgets
from django.forms import CheckboxSelectMultiple
from django.test import SimpleTestCase
from django.db.models import ManyToManyField
from .models import Band

def _unwrap_widget(field):
    widget = field.widget
    if isinstance(widget, widgets.RelatedFieldWidgetWrapper):
        return widget.widget
    return widget

from django import forms
from django.contrib import admin
from django.contrib.admin import widgets as admin_widgets
from django.test import SimpleTestCase
from django.db.models import ManyToManyField
from django.contrib.admin import site as default_admin_site
from django import forms
from django.contrib import admin
from django.contrib.admin import widgets as admin_widgets
from django.test import SimpleTestCase
from .models import Band
from django.db.models import ManyToManyField
from django.contrib.admin import site as default_admin_site

class ManyToManyWidgetPreservationTests(SimpleTestCase):
    """
    Regression tests for formfield_for_manytomany ensuring that an explicitly
    provided widget (either via formfield_overrides or kwargs) is preserved
    and get_autocomplete_fields is not called when a widget is present in kwargs.
    """

    def test_overrides_preserved_with_filter_vertical(self):

        class MyAdmin(admin.ModelAdmin):
            filter_vertical = ['members']
            formfield_overrides = {ManyToManyField: {'widget': forms.CheckboxSelectMultiple()}}

            def get_autocomplete_fields(self, request):
                if request is None:
                    raise RuntimeError('get_autocomplete_fields called with None')
                return super().get_autocomplete_fields(request)
        ma = MyAdmin(Band, default_admin_site)
        ff = ma.formfield_for_dbfield(Band._meta.get_field('members'), request=None)
        widget = self._unwrap_widget(ff)
        self.assertIsInstance(widget, forms.CheckboxSelectMultiple)

    def test_overrides_preserved_with_filter_horizontal(self):

        class MyAdmin(admin.ModelAdmin):
            filter_horizontal = ['members']
            formfield_overrides = {ManyToManyField: {'widget': forms.CheckboxSelectMultiple()}}

            def get_autocomplete_fields(self, request):
                if request is None:
                    raise RuntimeError('get_autocomplete_fields called with None')
                return super().get_autocomplete_fields(request)
        ma = MyAdmin(Band, default_admin_site)
        ff = ma.formfield_for_dbfield(Band._meta.get_field('members'), request=None)
        widget = self._unwrap_widget(ff)
        self.assertIsInstance(widget, forms.CheckboxSelectMultiple)

    def test_overrides_preserved_with_raw_id_fields(self):

        class MyAdmin(admin.ModelAdmin):
            raw_id_fields = ['members']
            formfield_overrides = {ManyToManyField: {'widget': forms.CheckboxSelectMultiple()}}

            def get_autocomplete_fields(self, request):
                if request is None:
                    raise RuntimeError('get_autocomplete_fields called with None')
                return super().get_autocomplete_fields(request)
        ma = MyAdmin(Band, default_admin_site)
        ff = ma.formfield_for_dbfield(Band._meta.get_field('members'), request=None)
        widget = self._unwrap_widget(ff)
        self.assertIsInstance(widget, forms.CheckboxSelectMultiple)

    def test_overrides_with_widget_class_preserved_filter_vertical(self):

        class MyAdmin(admin.ModelAdmin):
            filter_vertical = ['members']
            formfield_overrides = {ManyToManyField: {'widget': forms.CheckboxSelectMultiple}}

            def get_autocomplete_fields(self, request):
                if request is None:
                    raise RuntimeError('get_autocomplete_fields called with None')
                return super().get_autocomplete_fields(request)
        ma = MyAdmin(Band, default_admin_site)
        ff = ma.formfield_for_dbfield(Band._meta.get_field('members'), request=None)
        widget = self._unwrap_widget(ff)
        self.assertIsInstance(widget, forms.CheckboxSelectMultiple)

    def test_overrides_with_widget_class_preserved_raw_id(self):

        class MyAdmin(admin.ModelAdmin):
            raw_id_fields = ['members']
            formfield_overrides = {ManyToManyField: {'widget': forms.CheckboxSelectMultiple}}

            def get_autocomplete_fields(self, request):
                if request is None:
                    raise RuntimeError('get_autocomplete_fields called with None')
                return super().get_autocomplete_fields(request)
        ma = MyAdmin(Band, default_admin_site)
        ff = ma.formfield_for_dbfield(Band._meta.get_field('members'), request=None)
        widget = self._unwrap_widget(ff)
        self.assertIsInstance(widget, forms.CheckboxSelectMultiple)

from django import forms
from django.contrib import admin
from django.contrib.admin import widgets as admin_widgets
from django.db.models import ManyToManyField
from django.test import SimpleTestCase
from .models import Band, Advisor

class RegressionFormfieldForManyToManyTests(SimpleTestCase):

    def test_formfield_overrides_with_widget_class_does_not_call_get_autocomplete(self):

        class MyAdmin(admin.ModelAdmin):
            formfield_overrides = {ManyToManyField: {'widget': forms.CheckboxSelectMultiple}}

            def get_autocomplete_fields(self, request):
                if request is None:
                    raise AssertionError('get_autocomplete_fields() was called')
                return super().get_autocomplete_fields(request)
        ma = MyAdmin(Band, admin.site)
        ff = ma.formfield_for_dbfield(Band._meta.get_field('members'), request=None)
        widget = self._inner_widget(ff)
        self.assertIsInstance(widget, forms.CheckboxSelectMultiple)

    def test_formfield_overrides_with_widget_instance_does_not_call_get_autocomplete(self):

        class MyAdmin(admin.ModelAdmin):
            formfield_overrides = {ManyToManyField: {'widget': forms.CheckboxSelectMultiple()}}

            def get_autocomplete_fields(self, request):
                if request is None:
                    raise AssertionError('get_autocomplete_fields() was called')
                return super().get_autocomplete_fields(request)
        ma = MyAdmin(Band, admin.site)
        ff = ma.formfield_for_dbfield(Band._meta.get_field('members'), request=None)
        widget = self._inner_widget(ff)
        self.assertIsInstance(widget, forms.CheckboxSelectMultiple)

    def test_explicit_widget_kwarg_instance_does_not_call_get_autocomplete(self):

        class MyAdmin(admin.ModelAdmin):

            def get_autocomplete_fields(self, request):
                if request is None:
                    raise AssertionError('get_autocomplete_fields() was called')
                return super().get_autocomplete_fields(request)
        ma = MyAdmin(Band, admin.site)
        ff = ma.formfield_for_dbfield(Band._meta.get_field('members'), request=None, widget=forms.CheckboxSelectMultiple())
        widget = self._inner_widget(ff)
        self.assertIsInstance(widget, forms.CheckboxSelectMultiple)

    def test_explicit_widget_kwarg_class_does_not_call_get_autocomplete(self):

        class MyAdmin(admin.ModelAdmin):

            def get_autocomplete_fields(self, request):
                if request is None:
                    raise AssertionError('get_autocomplete_fields() was called')
                return super().get_autocomplete_fields(request)
        ma = MyAdmin(Band, admin.site)
        ff = ma.formfield_for_dbfield(Band._meta.get_field('members'), request=None, widget=forms.CheckboxSelectMultiple)
        widget = self._inner_widget(ff)
        self.assertTrue(isinstance(widget, forms.CheckboxSelectMultiple))

    def test_filter_vertical_with_formfield_override_widget_does_not_call_get_autocomplete(self):

        class MyAdmin(admin.ModelAdmin):
            filter_vertical = ['members']
            formfield_overrides = {ManyToManyField: {'widget': forms.CheckboxSelectMultiple}}

            def get_autocomplete_fields(self, request):
                if request is None:
                    raise AssertionError('get_autocomplete_fields() was called')
                return super().get_autocomplete_fields(request)
        ma = MyAdmin(Band, admin.site)
        ff = ma.formfield_for_dbfield(Band._meta.get_field('members'), request=None)
        widget = self._inner_widget(ff)
        self.assertIsInstance(widget, forms.CheckboxSelectMultiple)

    def test_filter_horizontal_with_formfield_override_widget_does_not_call_get_autocomplete(self):

        class MyAdmin(admin.ModelAdmin):
            filter_horizontal = ['members']
            formfield_overrides = {ManyToManyField: {'widget': forms.CheckboxSelectMultiple}}

            def get_autocomplete_fields(self, request):
                if request is None:
                    raise AssertionError('get_autocomplete_fields() was called')
                return super().get_autocomplete_fields(request)
        ma = MyAdmin(Band, admin.site)
        ff = ma.formfield_for_dbfield(Band._meta.get_field('members'), request=None)
        widget = self._inner_widget(ff)
        self.assertIsInstance(widget, forms.CheckboxSelectMultiple)

    def test_raw_id_fields_with_formfield_override_widget_does_not_call_get_autocomplete(self):

        class MyAdmin(admin.ModelAdmin):
            raw_id_fields = ['members']
            formfield_overrides = {ManyToManyField: {'widget': forms.CheckboxSelectMultiple}}

            def get_autocomplete_fields(self, request):
                if request is None:
                    raise AssertionError('get_autocomplete_fields() was called')
                return super().get_autocomplete_fields(request)
        ma = MyAdmin(Band, admin.site)
        ff = ma.formfield_for_dbfield(Band._meta.get_field('members'), request=None)
        widget = self._inner_widget(ff)
        self.assertIsInstance(widget, forms.CheckboxSelectMultiple)

    def test_autocomplete_field_present_but_formfield_overrides_widget_does_not_call_get_autocomplete(self):

        class MyAdmin(admin.ModelAdmin):
            autocomplete_fields = ['members']
            formfield_overrides = {ManyToManyField: {'widget': forms.CheckboxSelectMultiple}}

            def get_autocomplete_fields(self, request):
                if request is None:
                    raise AssertionError('get_autocomplete_fields() was called')
                return super().get_autocomplete_fields(request)
        ma = MyAdmin(Band, admin.site)
        ff = ma.formfield_for_dbfield(Band._meta.get_field('members'), request=None)
        widget = self._inner_widget(ff)
        self.assertIsInstance(widget, forms.CheckboxSelectMultiple)

    def test_autocomplete_field_present_but_explicit_widget_kwarg_does_not_call_get_autocomplete(self):

        class MyAdmin(admin.ModelAdmin):
            autocomplete_fields = ['members']

            def get_autocomplete_fields(self, request):
                if request is None:
                    raise AssertionError('get_autocomplete_fields() was called')
                return super().get_autocomplete_fields(request)
        ma = MyAdmin(Band, admin.site)
        ff = ma.formfield_for_dbfield(Band._meta.get_field('members'), request=None, widget=forms.CheckboxSelectMultiple())
        widget = self._inner_widget(ff)
        self.assertIsInstance(widget, forms.CheckboxSelectMultiple)

    def test_m2m_on_different_model_with_override_widget_does_not_call_get_autocomplete(self):

        class MyAdmin(admin.ModelAdmin):
            formfield_overrides = {ManyToManyField: {'widget': forms.CheckboxSelectMultiple}}

            def get_autocomplete_fields(self, request):
                if request is None:
                    raise AssertionError('get_autocomplete_fields() was called')
                return super().get_autocomplete_fields(request)
        ma = MyAdmin(Advisor, admin.site)
        ff = ma.formfield_for_dbfield(Advisor._meta.get_field('companies'), request=None)
        widget = self._inner_widget(ff)
        self.assertIsInstance(widget, forms.CheckboxSelectMultiple)