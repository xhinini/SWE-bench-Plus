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

from django import forms
from django.contrib import admin
from django.test import SimpleTestCase
from django.db.models import ManyToManyField
from django.contrib.admin import widgets as admin_widgets
from .models import Band

class ManyToManyAutocompleteCallTests(SimpleTestCase):
    """
    Regression tests for formfield_for_manytomany not to call
    get_autocomplete_fields() when a widget is explicitly provided.

    The candidate patch computed autocomplete_fields before checking for
    'widget' in kwargs which causes get_autocomplete_fields() to be called
    even when a widget is supplied. The gold patch avoids calling
    get_autocomplete_fields() in that case.
    """

    def test_m2m_widget_in_kwargs_checkbox_does_not_call_get_autocomplete(self):
        widget = forms.CheckboxSelectMultiple()

        class MyAdmin(admin.ModelAdmin):

            def get_autocomplete_fields(self, request):
                if request is None:
                    raise RuntimeError('get_autocomplete_fields called with None')
                return super().get_autocomplete_fields(request)
        ma = MyAdmin(Band, admin.site)
        ff = ma.formfield_for_manytomany(Band._meta.get_field('members'), request=None, widget=widget)
        inner = self._unwrap_widget(ff)
        self.assertIsInstance(inner, forms.CheckboxSelectMultiple)

    def test_m2m_widget_in_kwargs_select_multiple_does_not_call_get_autocomplete(self):
        widget = forms.SelectMultiple()

        class MyAdmin(admin.ModelAdmin):

            def get_autocomplete_fields(self, request):
                if request is None:
                    raise RuntimeError('get_autocomplete_fields called with None')
                return super().get_autocomplete_fields(request)
        ma = MyAdmin(Band, admin.site)
        ff = ma.formfield_for_manytomany(Band._meta.get_field('members'), request=None, widget=widget)
        inner = self._unwrap_widget(ff)
        self.assertIsInstance(inner, forms.SelectMultiple)

    def test_m2m_widget_in_formfield_overrides_checkbox_instance_does_not_call_get_autocomplete(self):
        widget = forms.CheckboxSelectMultiple()

        class MyAdmin(admin.ModelAdmin):
            formfield_overrides = {ManyToManyField: {'widget': widget}}

            def get_autocomplete_fields(self, request):
                if request is None:
                    raise RuntimeError('get_autocomplete_fields called with None')
                return super().get_autocomplete_fields(request)
        ma = MyAdmin(Band, admin.site)
        ff = ma.formfield_for_dbfield(Band._meta.get_field('members'), request=None)
        inner = self._unwrap_widget(ff)
        self.assertIsInstance(inner, forms.CheckboxSelectMultiple)

    def test_m2m_widget_in_formfield_overrides_select_instance_does_not_call_get_autocomplete(self):
        widget = forms.SelectMultiple()

        class MyAdmin(admin.ModelAdmin):
            formfield_overrides = {ManyToManyField: {'widget': widget}}

            def get_autocomplete_fields(self, request):
                if request is None:
                    raise RuntimeError('get_autocomplete_fields called with None')
                return super().get_autocomplete_fields(request)
        ma = MyAdmin(Band, admin.site)
        ff = ma.formfield_for_dbfield(Band._meta.get_field('members'), request=None)
        inner = self._unwrap_widget(ff)
        self.assertIsInstance(inner, forms.SelectMultiple)

    def test_m2m_widget_in_formfield_overrides_widget_instance_preserved_and_no_autocomplete_call(self):
        widget = forms.CheckboxSelectMultiple(attrs={'data-test': '1'})

        class MyAdmin(admin.ModelAdmin):
            formfield_overrides = {ManyToManyField: {'widget': widget}}

            def get_autocomplete_fields(self, request):
                if request is None:
                    raise RuntimeError('get_autocomplete_fields called with None')
                return super().get_autocomplete_fields(request)
        ma = MyAdmin(Band, admin.site)
        ff = ma.formfield_for_dbfield(Band._meta.get_field('members'), request=None)
        inner = self._unwrap_widget(ff)
        self.assertIsInstance(inner, forms.CheckboxSelectMultiple)
        self.assertEqual(inner.attrs.get('data-test'), '1')

    def test_m2m_widget_passed_directly_and_formfield_overrides_present_still_uses_direct_widget(self):
        override_widget = forms.SelectMultiple(attrs={'from_override': '1'})
        direct_widget = forms.CheckboxSelectMultiple(attrs={'direct': '1'})

        class MyAdmin(admin.ModelAdmin):
            formfield_overrides = {ManyToManyField: {'widget': override_widget}}

            def get_autocomplete_fields(self, request):
                if request is None:
                    raise RuntimeError('get_autocomplete_fields called with None')
                return super().get_autocomplete_fields(request)
        ma = MyAdmin(Band, admin.site)
        ff = ma.formfield_for_manytomany(Band._meta.get_field('members'), request=None, widget=direct_widget)
        inner = self._unwrap_widget(ff)
        self.assertIsInstance(inner, forms.CheckboxSelectMultiple)
        self.assertEqual(inner.attrs.get('direct'), '1')

    def test_m2m_widget_in_formfield_overrides_using_class_instance_does_not_call_get_autocomplete(self):
        widget = forms.CheckboxSelectMultiple(attrs={'a': 'b'})

        class MyAdmin(admin.ModelAdmin):
            formfield_overrides = {ManyToManyField: {'widget': widget}}

            def get_autocomplete_fields(self, request):
                if request is None:
                    raise RuntimeError('get_autocomplete_fields called with None')
                return super().get_autocomplete_fields(request)
        ma = MyAdmin(Band, admin.site)
        ff = ma.formfield_for_dbfield(Band._meta.get_field('members'), request=None)
        inner = self._unwrap_widget(ff)
        self.assertIsInstance(inner, forms.CheckboxSelectMultiple)
        self.assertEqual(inner.attrs.get('a'), 'b')

    def test_m2m_widget_kw_select_multiple_preserves_attrs_and_no_autocomplete_call(self):
        widget = forms.SelectMultiple(attrs={'foo': 'bar'})

        class MyAdmin(admin.ModelAdmin):

            def get_autocomplete_fields(self, request):
                if request is None:
                    raise RuntimeError('get_autocomplete_fields called with None')
                return super().get_autocomplete_fields(request)
        ma = MyAdmin(Band, admin.site)
        ff = ma.formfield_for_manytomany(Band._meta.get_field('members'), request=None, widget=widget)
        inner = self._unwrap_widget(ff)
        self.assertIsInstance(inner, forms.SelectMultiple)
        self.assertEqual(inner.attrs.get('foo'), 'bar')

    def test_m2m_formfield_overrides_widget_and_direct_widget_prefers_direct_and_no_autocomplete_call(self):
        override_widget = forms.SelectMultiple(attrs={'ov': '1'})
        direct_widget = forms.SelectMultiple(attrs={'dir': '1'})

        class MyAdmin(admin.ModelAdmin):
            formfield_overrides = {ManyToManyField: {'widget': override_widget}}

            def get_autocomplete_fields(self, request):
                if request is None:
                    raise RuntimeError('get_autocomplete_fields called with None')
                return super().get_autocomplete_fields(request)
        ma = MyAdmin(Band, admin.site)
        ff = ma.formfield_for_dbfield(Band._meta.get_field('members'), request=None, widget=direct_widget)
        inner = self._unwrap_widget(ff)
        self.assertIsInstance(inner, forms.SelectMultiple)
        self.assertEqual(inner.attrs.get('dir'), '1')

# No new imports required; tests reuse imports present in the existing test module.
from django import forms
from django.contrib import admin
from django.test import SimpleTestCase

from .models import Band, Advisor
from django.db.models import ManyToManyField


class ManyToManyFormfieldOverridesNoRequestTests(SimpleTestCase):
    """
    Regression tests for ensuring get_autocomplete_fields(request) is not
    called when a widget is provided via formfield_overrides and request is None.
    These would fail if get_autocomplete_fields() is invoked unconditionally
    (as in the candidate patch), but pass with the gold patch.
    """

    def _make_admin_raising_on_get_autocomplete(self, **admin_attrs):
        """
        Helper to create a ModelAdmin subclass that raises if
        get_autocomplete_fields is called with request is None.
        """
        class MyAdmin(admin.ModelAdmin):
            formfield_overrides = {
                ManyToManyField: {'widget': forms.CheckboxSelectMultiple}
            }
            # apply any attributes passed in
            pass
        for k, v in admin_attrs.items():
            setattr(MyAdmin, k, v)

        def get_autocomplete_fields(self, request):
            if request is None:
                raise RuntimeError("get_autocomplete_fields called with None")
            # fall back to the default implementation
            return admin.ModelAdmin.get_autocomplete_fields(self, request)

        MyAdmin.get_autocomplete_fields = get_autocomplete_fields
        return MyAdmin

    def test_filter_vertical_with_widget_override_does_not_call_get_autocomplete(self):
        MyAdmin = self._make_admin_raising_on_get_autocomplete(filter_vertical=['members'])
        ma = MyAdmin(Band, admin.site)
        field = ma.formfield_for_dbfield(Band._meta.get_field('members'), request=None)
        # formfield_overrides provided CheckboxSelectMultiple so the widget
        # used by the SelectMultiple should be CheckboxSelectMultiple.
        # The returned form field's widget may be wrapped; check inner widget.
        inner = getattr(field.widget, 'widget', field.widget)
        self.assertIsInstance(inner, forms.CheckboxSelectMultiple)

    def test_filter_horizontal_with_widget_override_does_not_call_get_autocomplete(self):
        MyAdmin = self._make_admin_raising_on_get_autocomplete(filter_horizontal=['members'])
        ma = MyAdmin(Band, admin.site)
        field = ma.formfield_for_dbfield(Band._meta.get_field('members'), request=None)
        inner = getattr(field.widget, 'widget', field.widget)
        self.assertIsInstance(inner, forms.CheckboxSelectMultiple)

    def test_raw_id_fields_with_widget_override_does_not_call_get_autocomplete(self):
        MyAdmin = self._make_admin_raising_on_get_autocomplete(raw_id_fields=['members'])
        ma = MyAdmin(Band, admin.site)
        field = ma.formfield_for_dbfield(Band._meta.get_field('members'), request=None)
        inner = getattr(field.widget, 'widget', field.widget)
        self.assertIsInstance(inner, forms.CheckboxSelectMultiple)

    def test_autocomplete_fields_with_widget_override_does_not_call_get_autocomplete(self):
        # even if the admin WOULD have an autocomplete field, providing a widget
        # via formfield_overrides must prevent get_autocomplete_fields from being
        # called when request is None.
        MyAdmin = self._make_admin_raising_on_get_autocomplete(autocomplete_fields=('members',))
        ma = MyAdmin(Band, admin.site)
        field = ma.formfield_for_dbfield(Band._meta.get_field('members'), request=None)
        inner = getattr(field.widget, 'widget', field.widget)
        self.assertIsInstance(inner, forms.CheckboxSelectMultiple)

    def test_combined_filters_with_widget_override_does_not_call_get_autocomplete(self):
        MyAdmin = self._make_admin_raising_on_get_autocomplete(
            filter_vertical=['members'], filter_horizontal=[]
        )
        ma = MyAdmin(Band, admin.site)
        field = ma.formfield_for_dbfield(Band._meta.get_field('members'), request=None)
        inner = getattr(field.widget, 'widget', field.widget)
        self.assertIsInstance(inner, forms.CheckboxSelectMultiple)

    def test_widget_override_instance_not_class_does_not_call_get_autocomplete(self):
        # Use an instance of the widget instead of the class
        class MyAdmin(admin.ModelAdmin):
            formfield_overrides = {ManyToManyField: {'widget': forms.CheckboxSelectMultiple()}}
            def get_autocomplete_fields(self, request):
                if request is None:
                    raise RuntimeError("get_autocomplete_fields called with None")
                return admin.ModelAdmin.get_autocomplete_fields(self, request)
        ma = MyAdmin(Band, admin.site)
        field = ma.formfield_for_dbfield(Band._meta.get_field('members'), request=None)
        inner = getattr(field.widget, 'widget', field.widget)
        self.assertIsInstance(inner, forms.CheckboxSelectMultiple)

    def test_multiple_admin_attributes_with_widget_override_does_not_call_get_autocomplete(self):
        MyAdmin = self._make_admin_raising_on_get_autocomplete(
            filter_vertical=['members'],
            raw_id_fields=['members'],
            autocomplete_fields=('members',)
        )
        ma = MyAdmin(Band, admin.site)
        field = ma.formfield_for_dbfield(Band._meta.get_field('members'), request=None)
        inner = getattr(field.widget, 'widget', field.widget)
        self.assertIsInstance(inner, forms.CheckboxSelectMultiple)

    def test_widget_override_on_different_m2m_field_does_not_call_get_autocomplete(self):
        # Use Advisor.companies many-to-many to ensure other model fields behave the same
        MyAdmin = self._make_admin_raising_on_get_autocomplete(filter_vertical=['companies'])
        ma = MyAdmin(Advisor, admin.site)
        field = ma.formfield_for_dbfield(Advisor._meta.get_field('companies'), request=None)
        inner = getattr(field.widget, 'widget', field.widget)
        self.assertIsInstance(inner, forms.CheckboxSelectMultiple)

    def test_widget_override_with_empty_filter_lists_does_not_call_get_autocomplete(self):
        MyAdmin = self._make_admin_raising_on_get_autocomplete(filter_vertical=[], filter_horizontal=[])
        ma = MyAdmin(Band, admin.site)
        field = ma.formfield_for_dbfield(Band._meta.get_field('members'), request=None)
        inner = getattr(field.widget, 'widget', field.widget)
        self.assertIsInstance(inner, forms.CheckboxSelectMultiple)

    def test_widget_override_with_no_admin_attrs_does_not_call_get_autocomplete(self):
        # Minimal case: only formfield_overrides present
        MyAdmin = self._make_admin_raising_on_get_autocomplete()
        ma = MyAdmin(Band, admin.site)
        field = ma.formfield_for_dbfield(Band._meta.get_field('members'), request=None)
        inner = getattr(field.widget, 'widget', field.widget)
        self.assertIsInstance(inner, forms.CheckboxSelectMultiple)

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

def _unwrap_widget(field):
    """Return the inner widget if the widget is wrapped by RelatedFieldWidgetWrapper."""
    widget = field.widget
    return getattr(widget, 'widget', widget)

from django import forms
from django.contrib import admin
from django.test import SimpleTestCase, override_settings
from django.contrib.admin import widgets as admin_widgets
from .models import Band
from django import forms
from django.contrib import admin
from django.test import SimpleTestCase, override_settings
from django.contrib.admin import widgets as admin_widgets
from .models import Band
from django.contrib.admin import AdminSite

@override_settings(ROOT_URLCONF='admin_widgets.urls')
class ManyToManyWidgetOverrideGuardTests(SimpleTestCase):
    """
    Guard tests to ensure get_autocomplete_fields is not called when a widget
    is explicitly provided for a ManyToManyField.
    """

    def _guard_admin_class(self):

        class GuardAdmin(admin.ModelAdmin):

            def get_autocomplete_fields(self, request):
                if request is None:
                    raise RuntimeError('get_autocomplete_fields called with None')
                return super().get_autocomplete_fields(request)
        return GuardAdmin

    def test_direct_manytomany_widget_kwarg_instance(self):
        AdminClass = self._guard_admin_class()
        ma = AdminClass(Band, admin.site)
        field = Band._meta.get_field('members')
        ff = ma.formfield_for_manytomany(field, request=None, widget=forms.CheckboxSelectMultiple())
        widget = self._unwrap_widget(ff)
        self.assertIsInstance(widget, forms.CheckboxSelectMultiple)

    def test_manytomany_widget_kwarg_via_formfield_for_dbfield(self):
        AdminClass = self._guard_admin_class()
        ma = AdminClass(Band, admin.site)
        field = Band._meta.get_field('members')
        ff = ma.formfield_for_dbfield(field, request=None, widget=forms.CheckboxSelectMultiple())
        widget = self._unwrap_widget(ff)
        self.assertIsInstance(widget, forms.CheckboxSelectMultiple)

    def test_formfield_overrides_widget_class_in_admin(self):

        class AdminWithOverride(self._guard_admin_class()):
            formfield_overrides = {field.__class__: {'widget': forms.CheckboxSelectMultiple} for field in (Band._meta.get_field('members'),)}
        ma = AdminWithOverride(Band, admin.site)
        field = Band._meta.get_field('members')
        ff = ma.formfield_for_dbfield(field, request=None)
        widget = self._unwrap_widget(ff)
        self.assertIsInstance(widget, forms.CheckboxSelectMultiple)

    def test_formfield_overrides_widget_instance_in_admin(self):

        class AdminWithOverride(self._guard_admin_class()):
            formfield_overrides = {Band._meta.get_field('members').__class__: {'widget': forms.CheckboxSelectMultiple()}}
        ma = AdminWithOverride(Band, admin.site)
        field = Band._meta.get_field('members')
        ff = ma.formfield_for_dbfield(field, request=None)
        widget = self._unwrap_widget(ff)
        self.assertIsInstance(widget, forms.CheckboxSelectMultiple)

    def test_widget_kwarg_with_raw_id_fields_present(self):

        class AdminWithRaw(self._guard_admin_class()):
            raw_id_fields = ['members']
        ma = AdminWithRaw(Band, admin.site)
        field = Band._meta.get_field('members')
        ff = ma.formfield_for_dbfield(field, request=None, widget=forms.CheckboxSelectMultiple())
        widget = self._unwrap_widget(ff)
        self.assertIsInstance(widget, forms.CheckboxSelectMultiple)

    def test_widget_kwarg_with_filter_vertical_present(self):

        class AdminWithFilter(self._guard_admin_class()):
            filter_vertical = ['members']
        ma = AdminWithFilter(Band, admin.site)
        field = Band._meta.get_field('members')
        ff = ma.formfield_for_dbfield(field, request=None, widget=forms.CheckboxSelectMultiple())
        widget = self._unwrap_widget(ff)
        self.assertIsInstance(widget, forms.CheckboxSelectMultiple)

    def test_widget_kwarg_with_filter_horizontal_present(self):

        class AdminWithFilter(self._guard_admin_class()):
            filter_horizontal = ['members']
        ma = AdminWithFilter(Band, admin.site)
        field = Band._meta.get_field('members')
        ff = ma.formfield_for_dbfield(field, request=None, widget=forms.CheckboxSelectMultiple())
        widget = self._unwrap_widget(ff)
        self.assertIsInstance(widget, forms.CheckboxSelectMultiple)

    def test_combined_formfield_overrides_and_raw_id_does_not_call_autocomplete(self):

        class AdminCombined(self._guard_admin_class()):
            raw_id_fields = ['members']
            formfield_overrides = {Band._meta.get_field('members').__class__: {'widget': forms.CheckboxSelectMultiple()}}
        ma = AdminCombined(Band, admin.site)
        field = Band._meta.get_field('members')
        ff = ma.formfield_for_dbfield(field, request=None)
        widget = self._unwrap_widget(ff)
        self.assertIsInstance(widget, forms.CheckboxSelectMultiple)

    def test_direct_manytomany_widget_kwarg_instance_multiple_calls(self):
        AdminClass = self._guard_admin_class()
        ma = AdminClass(Band, admin.site)
        field = Band._meta.get_field('members')
        for _ in range(3):
            ff = ma.formfield_for_manytomany(field, request=None, widget=forms.CheckboxSelectMultiple())
            widget = self._unwrap_widget(ff)
            self.assertIsInstance(widget, forms.CheckboxSelectMultiple)

    def test_formfield_overrides_widget_class_and_kwarg_priority(self):

        class AdminDual(self._guard_admin_class()):
            formfield_overrides = {Band._meta.get_field('members').__class__: {'widget': forms.Textarea}}
        ma = AdminDual(Band, admin.site)
        field = Band._meta.get_field('members')
        ff = ma.formfield_for_dbfield(field, request=None, widget=forms.CheckboxSelectMultiple())
        widget = self._unwrap_widget(ff)
        self.assertIsInstance(widget, forms.CheckboxSelectMultiple)

from django import forms
from django.test import SimpleTestCase
from django.contrib import admin
from django.contrib.admin import widgets
from django.db.models import ManyToManyField
from django.contrib.admin.tests import AdminSeleniumTestCase
from .models import Band, Member

class ManyToManyFormfieldForDBFieldRegressionTests(SimpleTestCase):

    def test_widget_kwarg_skips_get_autocomplete_fields_request_none(self):
        """
        If a widget is provided via kwargs to formfield_for_dbfield, get_autocomplete_fields()
        must not be called. Use a ModelAdmin subclass whose get_autocomplete_fields
        raises when called with a None request to detect incorrect calls.
        """

        class MyAdmin(admin.ModelAdmin):

            def get_autocomplete_fields(self, request):
                if request is None:
                    raise AssertionError('get_autocomplete_fields called with request=None')
                return super().get_autocomplete_fields(request)
        ma = MyAdmin(Band, admin.site)
        field = Band._meta.get_field('members')
        ff = ma.formfield_for_dbfield(field, request=None, widget=forms.CheckboxSelectMultiple())
        self.assertIsInstance(self.get_inner_widget(ff), forms.CheckboxSelectMultiple)

    def test_widget_kwarg_skips_get_autocomplete_fields_request_object(self):
        """
        Same as above, but pass a non-None dummy request. get_autocomplete_fields()
        should still not be invoked because 'widget' is in kwargs.
        """

        class MyAdmin(admin.ModelAdmin):

            def get_autocomplete_fields(self, request):
                raise AssertionError('get_autocomplete_fields should not be called')
        ma = MyAdmin(Band, admin.site)
        field = Band._meta.get_field('members')
        dummy_request = object()
        ff = ma.formfield_for_dbfield(field, request=dummy_request, widget=forms.CheckboxSelectMultiple())
        self.assertIsInstance(self.get_inner_widget(ff), forms.CheckboxSelectMultiple)

    def test_formfield_overrides_widget_skips_get_autocomplete_fields(self):
        """
        If a widget is provided via formfield_overrides for ManyToManyField,
        get_autocomplete_fields() should not be called (even if request is None).
        """

        class MyAdmin(admin.ModelAdmin):
            formfield_overrides = {ManyToManyField: {'widget': forms.CheckboxSelectMultiple()}}

            def get_autocomplete_fields(self, request):
                if request is None:
                    raise AssertionError('get_autocomplete_fields called with request=None')
                return super().get_autocomplete_fields(request)
        ma = MyAdmin(Band, admin.site)
        field = Band._meta.get_field('members')
        ff = ma.formfield_for_dbfield(field, request=None)
        self.assertIsInstance(self.get_inner_widget(ff), forms.CheckboxSelectMultiple)