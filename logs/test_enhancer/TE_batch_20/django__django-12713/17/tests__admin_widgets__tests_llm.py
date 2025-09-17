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

from django import forms
from django.test import SimpleTestCase
from django.contrib import admin
from django.contrib.admin import widgets
from django.db.models import ManyToManyField
from .models import Band

class ManyToManyWidgetOverrideTests(SimpleTestCase):
    """
    Tests to ensure that providing a widget (via kwargs or formfield_overrides)
    prevents formfield_for_manytomany from attempting to consult
    get_autocomplete_fields(request). This would raise if get_autocomplete_fields
    expected a non-None request and the request is None.
    """

    def test_widget_kwarg_prevents_get_autocomplete_call(self):

        class BadAutocompleteAdmin(admin.ModelAdmin):

            def get_autocomplete_fields(self, request):
                if request is None:
                    raise RuntimeError('get_autocomplete_fields should not be called')
                return super().get_autocomplete_fields(request)
        ma = BadAutocompleteAdmin(Band, admin.site)
        field = Band._meta.get_field('members')
        ff = ma.formfield_for_dbfield(field, request=None, widget=forms.CheckboxSelectMultiple())
        widget = self._unwrap_widget(ff)
        self.assertIsInstance(widget, forms.CheckboxSelectMultiple)

    def test_widget_in_formfield_overrides_prevents_get_autocomplete_call(self):

        class BadAutocompleteAdmin(admin.ModelAdmin):
            formfield_overrides = {ManyToManyField: {'widget': forms.CheckboxSelectMultiple}}

            def get_autocomplete_fields(self, request):
                if request is None:
                    raise RuntimeError('get_autocomplete_fields should not be called')
                return super().get_autocomplete_fields(request)
        ma = BadAutocompleteAdmin(Band, admin.site)
        field = Band._meta.get_field('members')
        ff = ma.formfield_for_dbfield(field, request=None)
        widget = self._unwrap_widget(ff)
        self.assertIsInstance(widget, forms.CheckboxSelectMultiple)

    def test_widget_kwarg_with_raw_id_fields_preserved(self):

        class BadAutocompleteAdmin(admin.ModelAdmin):
            raw_id_fields = ['members']

            def get_autocomplete_fields(self, request):
                if request is None:
                    raise RuntimeError('get_autocomplete_fields should not be called')
                return super().get_autocomplete_fields(request)
        ma = BadAutocompleteAdmin(Band, admin.site)
        field = Band._meta.get_field('members')
        ff = ma.formfield_for_dbfield(field, request=None, widget=forms.CheckboxSelectMultiple())
        widget = self._unwrap_widget(ff)
        self.assertIsInstance(widget, forms.CheckboxSelectMultiple)

    def test_widget_in_formfield_overrides_with_raw_id_fields_preserved(self):

        class BadAutocompleteAdmin(admin.ModelAdmin):
            raw_id_fields = ['members']
            formfield_overrides = {ManyToManyField: {'widget': forms.CheckboxSelectMultiple}}

            def get_autocomplete_fields(self, request):
                if request is None:
                    raise RuntimeError('get_autocomplete_fields should not be called')
                return super().get_autocomplete_fields(request)
        ma = BadAutocompleteAdmin(Band, admin.site)
        field = Band._meta.get_field('members')
        ff = ma.formfield_for_dbfield(field, request=None)
        widget = self._unwrap_widget(ff)
        self.assertIsInstance(widget, forms.CheckboxSelectMultiple)

    def test_widget_kwarg_with_filter_vertical_preserved(self):

        class BadAutocompleteAdmin(admin.ModelAdmin):
            filter_vertical = ['members']

            def get_autocomplete_fields(self, request):
                if request is None:
                    raise RuntimeError('get_autocomplete_fields should not be called')
                return super().get_autocomplete_fields(request)
        ma = BadAutocompleteAdmin(Band, admin.site)
        field = Band._meta.get_field('members')
        ff = ma.formfield_for_dbfield(field, request=None, widget=forms.CheckboxSelectMultiple())
        widget = self._unwrap_widget(ff)
        self.assertIsInstance(widget, forms.CheckboxSelectMultiple)

    def test_widget_in_formfield_overrides_with_filter_horizontal_preserved(self):

        class BadAutocompleteAdmin(admin.ModelAdmin):
            filter_horizontal = ['members']
            formfield_overrides = {ManyToManyField: {'widget': forms.CheckboxSelectMultiple}}

            def get_autocomplete_fields(self, request):
                if request is None:
                    raise RuntimeError('get_autocomplete_fields should not be called')
                return super().get_autocomplete_fields(request)
        ma = BadAutocompleteAdmin(Band, admin.site)
        field = Band._meta.get_field('members')
        ff = ma.formfield_for_dbfield(field, request=None)
        widget = self._unwrap_widget(ff)
        self.assertIsInstance(widget, forms.CheckboxSelectMultiple)

    def test_widget_kwarg_overrides_autocomplete_setting(self):

        class BadAutocompleteAdmin(admin.ModelAdmin):

            def get_autocomplete_fields(self, request):
                if request is None:
                    raise RuntimeError('get_autocomplete_fields should not be called')
                return ('members',)
        ma = BadAutocompleteAdmin(Band, admin.site)
        field = Band._meta.get_field('members')
        ff = ma.formfield_for_dbfield(field, request=None, widget=forms.CheckboxSelectMultiple())
        widget = self._unwrap_widget(ff)
        self.assertIsInstance(widget, forms.CheckboxSelectMultiple)

    def test_widget_in_formfield_overrides_overrides_autocomplete_setting(self):

        class BadAutocompleteAdmin(admin.ModelAdmin):
            formfield_overrides = {ManyToManyField: {'widget': forms.CheckboxSelectMultiple}}

            def get_autocomplete_fields(self, request):
                if request is None:
                    raise RuntimeError('get_autocomplete_fields should not be called')
                return ('members',)
        ma = BadAutocompleteAdmin(Band, admin.site)
        field = Band._meta.get_field('members')
        ff = ma.formfield_for_dbfield(field, request=None)
        widget = self._unwrap_widget(ff)
        self.assertIsInstance(widget, forms.CheckboxSelectMultiple)

    def test_selectmultiple_help_text_appended_when_selectmultiple_widget_provided(self):

        class BadAutocompleteAdmin(admin.ModelAdmin):

            def get_autocomplete_fields(self, request):
                if request is None:
                    raise RuntimeError('get_autocomplete_fields should not be called')
                return ()
        ma = BadAutocompleteAdmin(Band, admin.site)
        field = Band._meta.get_field('members')
        ff = ma.formfield_for_dbfield(field, request=None, widget=forms.SelectMultiple())
        self.assertIn('Hold down', ff.help_text or '')

from django import forms
from django.contrib import admin
from django.test import SimpleTestCase
from django.db.models import ManyToManyField
from django.contrib.admin import widgets as admin_widgets
from .models import Band, Advisor, Company

class RegressionFormfieldForManyToManyTests(SimpleTestCase):
    """
    Regression tests for formfield_for_manytomany to ensure that when a
    widget is already supplied (via formfield_overrides or kwargs) the
    admin does not call get_autocomplete_fields(request) when request is
    None.
    """

    def test_formfield_overrides_class_widget_avoids_get_autocomplete_fields(self):
        ma = self._make_admin_with_override(forms.CheckboxSelectMultiple)
        self._assert_override_used(ma, request=None)

    def test_formfield_overrides_instance_widget_avoids_get_autocomplete_fields(self):
        ma = self._make_admin_with_override(forms.CheckboxSelectMultiple())
        self._assert_override_used(ma, request=None)

    def test_formfield_overrides_with_filter_vertical_avoids_get_autocomplete_fields(self):
        ma = self._make_admin_with_override(forms.CheckboxSelectMultiple, extra_attrs={'filter_vertical': ['members']})
        self._assert_override_used(ma, request=None)

    def test_formfield_overrides_with_filter_horizontal_avoids_get_autocomplete_fields(self):
        ma = self._make_admin_with_override(forms.CheckboxSelectMultiple, extra_attrs={'filter_horizontal': ['members']})
        self._assert_override_used(ma, request=None)

    def test_formfield_overrides_with_autocomplete_fields_avoids_get_autocomplete_fields(self):
        ma = self._make_admin_with_override(forms.CheckboxSelectMultiple, extra_attrs={'autocomplete_fields': ('members',)})
        self._assert_override_used(ma, request=None)

    def test_formfield_overrides_with_raw_id_fields_avoids_get_autocomplete_fields(self):
        ma = self._make_admin_with_override(forms.CheckboxSelectMultiple, extra_attrs={'raw_id_fields': ['members']})
        self._assert_override_used(ma, request=None)

    def test_formfield_overrides_with_multiple_attrs_avoids_get_autocomplete_fields(self):
        ma = self._make_admin_with_override(forms.CheckboxSelectMultiple(), extra_attrs={'filter_vertical': ['members'], 'autocomplete_fields': ('members',)})
        self._assert_override_used(ma, request=None)

    def test_explicit_widget_kwarg_to_formfield_for_manytomany_avoids_get_autocomplete_fields(self):

        class RaisingAdminDirect(admin.ModelAdmin):

            def get_autocomplete_fields(self, request):
                if request is None:
                    raise AssertionError('get_autocomplete_fields called with None')
                return super().get_autocomplete_fields(request)
        ma = RaisingAdminDirect(Band, admin.site)
        db_field = Band._meta.get_field('members')
        ff = ma.formfield_for_manytomany(db_field, request=None, widget=forms.CheckboxSelectMultiple())
        widget = ff.widget
        self.assertIsInstance(widget, forms.CheckboxSelectMultiple)

    def test_formfield_overrides_on_different_model_field_name_avoids_get_autocomplete_fields(self):

        class RaisingAdminAdvisor(admin.ModelAdmin):
            formfield_overrides = {ManyToManyField: {'widget': forms.CheckboxSelectMultiple}}
            raw_id_fields = ['companies']

            def get_autocomplete_fields(self, request):
                if request is None:
                    raise AssertionError('get_autocomplete_fields called with None')
                return super().get_autocomplete_fields(request)
        ma = RaisingAdminAdvisor(Advisor, admin.site)
        ff = ma.formfield_for_dbfield(Advisor._meta.get_field('companies'), request=None)
        if isinstance(ff.widget, admin_widgets.RelatedFieldWidgetWrapper):
            widget = ff.widget.widget
        else:
            widget = ff.widget
        self.assertIsInstance(widget, forms.CheckboxSelectMultiple)

from django import forms
from django.test import SimpleTestCase
from django.contrib import admin
from django.contrib.admin import widgets
from django.db.models import ManyToManyField
from .models import Band

class FormfieldForManyToManyWidgetOverrideTests(SimpleTestCase):

    def test_formfield_overrides_widget_instance_prevents_get_autocomplete_call(self):

        class MyAdmin(admin.ModelAdmin):
            formfield_overrides = {ManyToManyField: {'widget': forms.CheckboxSelectMultiple()}}
        ma = MyAdmin(Band, admin.site)

        def bad_get_autocomplete(request):
            raise AssertionError('get_autocomplete_fields should not be called')
        ma.get_autocomplete_fields = bad_get_autocomplete
        f = ma.formfield_for_dbfield(Band._meta.get_field('members'), request=None)
        self.assertIsInstance(f.widget.widget, forms.CheckboxSelectMultiple)

    def test_formfield_overrides_widget_class_prevents_get_autocomplete_call(self):

        class MyAdmin(admin.ModelAdmin):
            formfield_overrides = {ManyToManyField: {'widget': forms.CheckboxSelectMultiple}}
        ma = MyAdmin(Band, admin.site)

        def bad_get_autocomplete(request):
            raise AssertionError('get_autocomplete_fields should not be called')
        ma.get_autocomplete_fields = bad_get_autocomplete
        f = ma.formfield_for_dbfield(Band._meta.get_field('members'), request=None)
        self.assertIsInstance(f.widget.widget, forms.CheckboxSelectMultiple)

from django import forms
from django.test import SimpleTestCase
from django.contrib import admin
from django.contrib.admin import widgets
from .models import Band, Advisor, School

class M2MWidgetKwargsTests(SimpleTestCase):
    """
    Ensure that providing a 'widget' kwarg prevents any calls to
    get_autocomplete_fields() (or other side-effecting logic) in
    formfield_for_manytomany/formfield_for_dbfield.
    """

    def _make_admin_that_errors_on_autocomplete(self):

        class ErroringAdmin(admin.ModelAdmin):

            def get_autocomplete_fields(self, request):
                raise AssertionError("get_autocomplete_fields() should not be called when 'widget' is provided")
        return ErroringAdmin

    def test_band_members_widget_kwarg_no_request(self):
        AdminClass = self._make_admin_that_errors_on_autocomplete()
        ma = AdminClass(Band, admin.site)
        ff = ma.formfield_for_dbfield(Band._meta.get_field('members'), request=None, widget=forms.CheckboxSelectMultiple())
        widget = self._unwrap_widget(ff)
        self.assertIsInstance(widget, forms.CheckboxSelectMultiple)

    def test_band_members_widget_kwarg_with_request(self):
        AdminClass = self._make_admin_that_errors_on_autocomplete()
        ma = AdminClass(Band, admin.site)
        dummy_request = object()
        ff = ma.formfield_for_dbfield(Band._meta.get_field('members'), request=dummy_request, widget=forms.CheckboxSelectMultiple())
        widget = self._unwrap_widget(ff)
        self.assertIsInstance(widget, forms.CheckboxSelectMultiple)

    def test_advisor_companies_widget_kwarg_no_request(self):
        AdminClass = self._make_admin_that_errors_on_autocomplete()
        ma = AdminClass(Advisor, admin.site)
        ff = ma.formfield_for_dbfield(Advisor._meta.get_field('companies'), request=None, widget=forms.CheckboxSelectMultiple())
        widget = self._unwrap_widget(ff)
        self.assertIsInstance(widget, forms.CheckboxSelectMultiple)

    def test_advisor_companies_widget_kwarg_with_request(self):
        AdminClass = self._make_admin_that_errors_on_autocomplete()
        ma = AdminClass(Advisor, admin.site)
        dummy_request = object()
        ff = ma.formfield_for_dbfield(Advisor._meta.get_field('companies'), request=dummy_request, widget=forms.CheckboxSelectMultiple())
        widget = self._unwrap_widget(ff)
        self.assertIsInstance(widget, forms.CheckboxSelectMultiple)

    def test_school_students_widget_kwarg_no_request(self):
        AdminClass = self._make_admin_that_errors_on_autocomplete()
        ma = AdminClass(School, admin.site)
        ff = ma.formfield_for_dbfield(School._meta.get_field('students'), request=None, widget=forms.CheckboxSelectMultiple())
        widget = self._unwrap_widget(ff)
        self.assertIsInstance(widget, forms.CheckboxSelectMultiple)

    def test_school_students_widget_kwarg_with_request(self):
        AdminClass = self._make_admin_that_errors_on_autocomplete()
        ma = AdminClass(School, admin.site)
        dummy_request = object()
        ff = ma.formfield_for_dbfield(School._meta.get_field('students'), request=dummy_request, widget=forms.CheckboxSelectMultiple())
        widget = self._unwrap_widget(ff)
        self.assertIsInstance(widget, forms.CheckboxSelectMultiple)

    def test_school_alumni_widget_kwarg_no_request(self):
        AdminClass = self._make_admin_that_errors_on_autocomplete()
        ma = AdminClass(School, admin.site)
        ff = ma.formfield_for_dbfield(School._meta.get_field('alumni'), request=None, widget=forms.CheckboxSelectMultiple())
        widget = self._unwrap_widget(ff)
        self.assertIsInstance(widget, forms.CheckboxSelectMultiple)

    def test_school_alumni_widget_kwarg_with_request(self):
        AdminClass = self._make_admin_that_errors_on_autocomplete()
        ma = AdminClass(School, admin.site)
        dummy_request = object()
        ff = ma.formfield_for_dbfield(School._meta.get_field('alumni'), request=dummy_request, widget=forms.CheckboxSelectMultiple())
        widget = self._unwrap_widget(ff)
        self.assertIsInstance(widget, forms.CheckboxSelectMultiple)

    def test_direct_formfield_for_manytomany_widget_kwarg_no_request(self):
        AdminClass = self._make_admin_that_errors_on_autocomplete()
        ma = AdminClass(Band, admin.site)
        ff = ma.formfield_for_manytomany(Band._meta.get_field('members'), request=None, widget=forms.CheckboxSelectMultiple())
        widget = self._unwrap_widget(ff)
        self.assertIsInstance(widget, forms.CheckboxSelectMultiple)

from django import forms
from django.contrib import admin
from django.contrib.admin import widgets as admin_widgets
from django import forms
from django.contrib import admin
from django.contrib.admin import widgets as admin_widgets
from django.test import SimpleTestCase
from .models import Band
from django.contrib.admin import widgets

def _unwrap_widget(field):
    """
    Unwrap RelatedFieldWidgetWrapper if present to get the underlying widget.
    """
    w = field.widget
    if isinstance(w, widgets.RelatedFieldWidgetWrapper):
        return w.widget
    return w

from django import forms
from django.contrib import admin
from django.db.models import ManyToManyField
from django.test import SimpleTestCase
from .models import Band
from django import forms
from django.contrib import admin
from django.db.models import ManyToManyField
from django.test import SimpleTestCase
from .models import Band

def _inner_widget(field):
    """
    Return the actual inner widget (unwrapping RelatedFieldWidgetWrapper
    if present), matching the pattern used in existing tests.
    """
    widget = field.widget
    return getattr(widget, 'widget', widget)

from django import forms
from django.test import SimpleTestCase
from django.contrib import admin
from django.db.models import ManyToManyField
from django.contrib.admin import widgets as admin_widgets
from .models import Band, Member

def _unwrap_widget(field):
    w = field.widget
    return getattr(w, 'widget', w)

from django import forms
from django.contrib import admin
from django.contrib.admin import widgets
from django.test import SimpleTestCase
from django.db.models import ManyToManyField
from .models import Band, Advisor

class ManyToManyWidgetOverrideTests(SimpleTestCase):

    def test_get_autocomplete_fields_not_called_when_widget_overridden(self):
        """
        If a ModelAdmin overrides get_autocomplete_fields to raise when
        request is None, providing a widget via formfield_overrides must
        prevent that method from being called. The candidate patch calls
        get_autocomplete_fields unconditionally, which would raise here.
        """

        class BandAdmin(admin.ModelAdmin):
            formfield_overrides = {ManyToManyField: {'widget': forms.CheckboxSelectMultiple}}

            def get_autocomplete_fields(self, request):
                if request is None:
                    raise RuntimeError('get_autocomplete_fields must not be called with request=None')
                return super().get_autocomplete_fields(request)
        ma = BandAdmin(Band, admin.site)
        ff = ma.formfield_for_dbfield(Band._meta.get_field('members'), request=None)
        widget = ff.widget
        if isinstance(widget, widgets.RelatedFieldWidgetWrapper):
            widget = widget.widget
        self.assertIsInstance(widget, forms.CheckboxSelectMultiple)

    def test_get_autocomplete_fields_not_called_when_widget_in_kwargs(self):
        """
        Similar to above, but when widget is passed explicitly to
        formfield_for_manytomany via kwargs.
        """

        class BandAdmin(admin.ModelAdmin):

            def get_autocomplete_fields(self, request):
                if request is None:
                    raise RuntimeError('get_autocomplete_fields must not be called with request=None')
                return super().get_autocomplete_fields(request)
        ma = BandAdmin(Band, admin.site)
        field = Band._meta.get_field('members')
        ff = ma.formfield_for_manytomany(field, request=None, widget=forms.CheckboxSelectMultiple())
        widget = ff.widget
        if isinstance(widget, widgets.RelatedFieldWidgetWrapper):
            widget = widget.widget
        self.assertIsInstance(widget, forms.CheckboxSelectMultiple)

from django import forms
from django.contrib import admin
from django.contrib.admin import widgets as admin_widgets
from django.db.models import ManyToManyField
from django.test import SimpleTestCase
from .models import Band, Advisor, School, Member
from django import forms
from django.contrib import admin
from django.contrib.admin import widgets as admin_widgets
from django.test import SimpleTestCase
from django.db.models import ManyToManyField
from django.contrib.admin.tests import AdminSeleniumTestCase
from .models import Band, Advisor, School, Member

class ManyToManyWidgetOverrideTests(SimpleTestCase):

    def test_formfield_overrides_preserve_widget_band_members(self):
        """
        If formfield_overrides provides a widget for a M2M field, that widget
        must be used and get_autocomplete_fields must NOT be called (request=None).
        """

        class BadAutocompleteAdmin(admin.ModelAdmin):
            formfield_overrides = {ManyToManyField: {'widget': forms.CheckboxSelectMultiple()}}

            def get_autocomplete_fields(self, request):
                return ['members'] if request.user.is_staff else []
        ma = BadAutocompleteAdmin(Band, admin.site)
        ff = ma.formfield_for_dbfield(Band._meta.get_field('members'), request=None)
        widget = self._get_unwrapped_widget(ff)
        self.assertIsInstance(widget, forms.CheckboxSelectMultiple)

    def test_formfield_overrides_preserve_widget_advisor_companies(self):

        class BadAutocompleteAdmin(admin.ModelAdmin):
            formfield_overrides = {ManyToManyField: {'widget': forms.CheckboxSelectMultiple()}}

            def get_autocomplete_fields(self, request):
                return ['companies'] if request.user.is_superuser else []
        ma = BadAutocompleteAdmin(Advisor, admin.site)
        ff = ma.formfield_for_dbfield(Advisor._meta.get_field('companies'), request=None)
        widget = self._get_unwrapped_widget(ff)
        self.assertIsInstance(widget, forms.CheckboxSelectMultiple)

    def test_formfield_overrides_preserve_widget_school_alumni(self):

        class BadAutocompleteAdmin(admin.ModelAdmin):
            formfield_overrides = {ManyToManyField: {'widget': forms.CheckboxSelectMultiple()}}

            def get_autocomplete_fields(self, request):
                if request.user:
                    return ['alumni']
                return []
        ma = BadAutocompleteAdmin(School, admin.site)
        ff = ma.formfield_for_dbfield(School._meta.get_field('alumni'), request=None)
        widget = self._get_unwrapped_widget(ff)
        self.assertIsInstance(widget, forms.CheckboxSelectMultiple)

    def test_explicit_widget_kwarg_preserved_band_members(self):
        """
        Passing a widget explicitly via kwargs to formfield_for_dbfield should
        prevent any call to get_autocomplete_fields that expects a request.
        """

        class BadAutocompleteAdmin(admin.ModelAdmin):

            def get_autocomplete_fields(self, request):
                return ['members'] if request.user.is_anonymous else []
        ma = BadAutocompleteAdmin(Band, admin.site)
        ff = ma.formfield_for_dbfield(Band._meta.get_field('members'), request=None, widget=forms.CheckboxSelectMultiple())
        widget = self._get_unwrapped_widget(ff)
        self.assertIsInstance(widget, forms.CheckboxSelectMultiple)

    def test_filter_horizontal_override_preserve_widget(self):

        class BadAutocompleteAdmin(admin.ModelAdmin):
            filter_horizontal = ['members']
            formfield_overrides = {ManyToManyField: {'widget': forms.CheckboxSelectMultiple()}}

            def get_autocomplete_fields(self, request):
                return ['members'] if bool(request.user) else []
        ma = BadAutocompleteAdmin(Band, admin.site)
        ff = ma.formfield_for_dbfield(Band._meta.get_field('members'), request=None)
        widget = self._get_unwrapped_widget(ff)
        self.assertIsInstance(widget, forms.CheckboxSelectMultiple)

    def test_raw_id_fields_override_preserve_widget(self):

        class BadAutocompleteAdmin(admin.ModelAdmin):
            raw_id_fields = ['members']
            formfield_overrides = {ManyToManyField: {'widget': forms.CheckboxSelectMultiple()}}

            def get_autocomplete_fields(self, request):
                return ['members'] if request.user.is_staff else []
        ma = BadAutocompleteAdmin(Band, admin.site)
        ff = ma.formfield_for_dbfield(Band._meta.get_field('members'), request=None)
        widget = self._get_unwrapped_widget(ff)
        self.assertIsInstance(widget, forms.CheckboxSelectMultiple)

    def test_autocomplete_field_name_override_preserve_widget(self):
        """
        Even if the admin defines an autocomplete field name, a provided widget
        from formfield_overrides should be respected and no request-based
        calls should be attempted when request is None.
        """

        class BadAutocompleteAdmin(admin.ModelAdmin):
            autocomplete_fields = ('members',)
            formfield_overrides = {ManyToManyField: {'widget': forms.CheckboxSelectMultiple()}}

            def get_autocomplete_fields(self, request):
                return list(self.autocomplete_fields) if request.user else []
        ma = BadAutocompleteAdmin(Band, admin.site)
        ff = ma.formfield_for_dbfield(Band._meta.get_field('members'), request=None)
        widget = self._get_unwrapped_widget(ff)
        self.assertIsInstance(widget, forms.CheckboxSelectMultiple)

from django import forms
from django.contrib import admin
from django.contrib.admin import widgets
from django.test import SimpleTestCase
from django.db.models import ManyToManyField
from django import forms
from django.contrib import admin
from django.contrib.admin import widgets
from django.test import SimpleTestCase
from django.db.models import ManyToManyField
from .models import Band, Member

def _unwrap_widget(field):
    """
    Helper to unwrap RelatedFieldWidgetWrapper if present and return the inner widget.
    Accepts a form field instance (as returned by formfield_for_dbfield / formfield_for_manytomany).
    """
    w = field.widget
    if isinstance(w, widgets.RelatedFieldWidgetWrapper):
        return w.widget
    return w