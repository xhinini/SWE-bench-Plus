from django.contrib.admin.options import ModelAdmin
from django.db.models import Field, Model, CharField, ManyToManyField
from django.contrib.admin.sites import AdminSite
from django.core.checks import Error
from django.test import SimpleTestCase
from django.contrib.admin.options import ModelAdmin
from django.db.models import Field, Model, CharField, ManyToManyField
from django.contrib.admin.sites import AdminSite
from django.core.checks import Error
from django.test import SimpleTestCase
from .models import ValidationTestModel, ValidationTestInlineModel

class AdditionalListDisplayRegressionTests(SimpleTestCase):

    def test_staticmethod_on_model_is_valid(self):

        class SModel(Model):
            name = CharField(max_length=10)

            @staticmethod
            def helper():
                return 'ok'

            class Meta:
                app_label = 'modeladmin'

        class SAdmin(ModelAdmin):
            list_display = ('helper',)
        self.assertCheckEquals(SAdmin, SModel, [])

    def test_property_raises_on_class_access_handled_correctly(self):

        class PModel(Model):
            value = CharField(max_length=10)

            @property
            def computed(self):
                return self.value + 'x'

            class Meta:
                app_label = 'modeladmin'

        class PAdmin(ModelAdmin):
            list_display = ('computed',)
        self.assertCheckEquals(PAdmin, PModel, [])

from django.contrib.admin.options import ModelAdmin
from django.contrib.admin.sites import AdminSite
from django.core.checks import Error
from django.db import models
from django.test import SimpleTestCase
from django.contrib.admin.options import ModelAdmin
from django.contrib.admin.sites import AdminSite
from django.core.checks import Error
from django.db import models
from django.test import SimpleTestCase

class ListDisplayRegressionTests(SimpleTestCase):

    def test_admin_attribute_takes_precedence_over_model_many_to_many(self):

        class Other(models.Model):

            class Meta:
                app_label = 'list_display_tests'

        class TestModel(models.Model):
            others = models.ManyToManyField(Other)

            class Meta:
                app_label = 'list_display_tests'

        class TestAdmin(ModelAdmin):

            def others(self, obj):
                return 'admin-provided'
            list_display = ('others',)
        ids, errors = self._check(TestAdmin, TestModel)
        self.assertNotIn('admin.E109', ids)
        self.assertEqual(ids, [])

from django.contrib.admin.options import ModelAdmin
from django.db import models
from django.contrib.admin.sites import AdminSite
from .test_checks import CheckTestCase

class ListDisplayRegressionTests(CheckTestCase):

    def test_admin_non_callable_attribute_masks_many_to_many_and_is_valid(self):
        """
        If the ModelAdmin defines a non-callable attribute with the same name
        as a model attribute, it's treated as an admin attribute and should be
        accepted (legacy behavior).
        """

        class Other(models.Model):

            class Meta:
                app_label = 'testsapp'

        class Thing(models.Model):
            others = models.ManyToManyField(Other)

            class Meta:
                app_label = 'testsapp'

        class TestModelAdmin(ModelAdmin):
            others = 'masked-value'
            list_display = ('others',)
        self.assertIsValid(TestModelAdmin, Thing)

    def test_field_descriptor_on_model_class_but_not_a_model_field_is_valid(self):
        """
        If the model class exposes a class-level descriptor or attribute that
        is not a Field (e.g., a plain attribute or function), it should be
        accepted in list_display.
        """

        class M(models.Model):

            class Meta:
                app_label = 'testsapp'
            sample_value = 42

            def sample_method(self):
                return 'ok'

        class TestModelAdmin(ModelAdmin):
            list_display = ('sample_value', 'sample_method')
        self.assertIsValid(TestModelAdmin, M)

from django.db.models import Model, Field
from django.contrib.admin.options import ModelAdmin
from django.core.checks import Error
from django.test import SimpleTestCase
from django.db.models import Model, Field
from django.contrib.admin.sites import AdminSite
from .models import ValidationTestModel

class ListDisplayRegressionTests(SimpleTestCase):

    def test_descriptor_that_raises_attributeerror_is_reported_as_missing_E108(self):

        class BadDescriptor:

            def __get__(self, instance, owner):
                raise AttributeError()

        class TestModel(Model):
            attr = BadDescriptor()

            class Meta:
                app_label = 'myapp'

        class TestModelAdmin(ModelAdmin):
            list_display = ('attr',)
        self.assertIsInvalid(TestModelAdmin, TestModel, "The value of 'list_display[0]' refers to 'attr', which is not a callable, an attribute of 'TestModelAdmin', or an attribute or method on 'myapp.TestModel'.", 'admin.E108')

from django.contrib.admin.options import ModelAdmin
from django.contrib.admin.sites import AdminSite
from django.core.checks import Error
from django.db import models
from django.test import SimpleTestCase
from .test_checks import CheckTestCase

class ListDisplayRegressionTests(CheckTestCase):

    def test_descriptor_accessible_only_via_instance_is_valid(self):

        class PositionField(models.Field):

            def contribute_to_class(self, cls, name):
                super().contribute_to_class(cls, name)
                setattr(cls, self.name, self)

            def __get__(self, instance, owner):
                if instance is None:
                    raise AttributeError('Only via instance')
                return 0

            def deconstruct(self):
                name, path, args, kwargs = super().deconstruct()
                return (name, path, args, kwargs)

            def db_type(self, connection):
                return 'integer'

        class TestModel(models.Model):
            order = PositionField()

            class Meta:
                app_label = 'modeladmin'

        class TestAdmin(ModelAdmin):
            list_display = ('order',)
        self.assertIsValid(TestAdmin, TestModel)

from django.contrib.admin.options import ModelAdmin
from django.test import SimpleTestCase
from django.db.models import Model, Field, ManyToManyField
from django.contrib.admin.sites import AdminSite
from django.core.checks import Error
from .test_checks import CheckTestCase

class AdditionalListDisplayEdgeCases(CheckTestCase):

    def test_attribute_of_model_class_that_is_not_callable_nor_field_errors(self):
        """
        If the model class has an attribute that is not callable and does not
        correspond to a field, it should be treated as present and not raise
        the missing-field error (i.e. it's acceptable). The check should not
        raise admin.E108 in that case.
        """

        class Thing(Model):

            class Meta:
                app_label = 'tests'
        Thing.static = 123

        class ThingAdmin(ModelAdmin):
            list_display = ('static',)
        self.assertIsValid(ThingAdmin, Thing)

from django.contrib.admin.sites import AdminSite
from django.contrib.admin.options import ModelAdmin
from django.core.checks import Error
from django.db import models
from django.test import SimpleTestCase
from django.contrib.admin.sites import AdminSite
from django.contrib.admin.options import ModelAdmin
from django.core.checks import Error
from django.db import models
from django.test import SimpleTestCase

class AdditionalListDisplayChecks(SimpleTestCase):

    def test_admin_function_object_in_list_display_is_valid(self):

        class M(models.Model):

            class Meta:
                app_label = 'tests'

        def func(obj):
            return 'x'

        class A(ModelAdmin):
            list_display = (func,)
        errors = self._errors_for(A, M)
        self.assertEqual(errors, [])

from django.test import SimpleTestCase
from django.contrib.admin.options import ModelAdmin
from django.contrib.admin.sites import AdminSite
from django.core.checks import Error
from django.db.models import Model, ManyToManyField, IntegerField, Field
from django.db import models

def run_list_display_check(list_display, model_cls, admin_attrs=None):
    admin_attrs = admin_attrs or {}

    class TestAdmin(ModelAdmin):
        pass
    for name, val in admin_attrs.items():
        setattr(TestAdmin, name, val)
    TestAdmin.list_display = list_display
    admin_obj = TestAdmin(model_cls, AdminSite())
    return admin_obj.check()

from django.contrib.admin.options import ModelAdmin
from django.contrib.admin.sites import AdminSite
from django.db import models
from django.db.models import Model
from django.test import SimpleTestCase
from .test_checks import CheckTestCase

class ListDisplayRegressionTests(CheckTestCase):

    def test_many_to_many_after_callable_reports_correct_index(self):

        class Other(Model):
            name = models.CharField(max_length=10)

            class Meta:
                app_label = 'tests'

        class Thing(Model):
            others = models.ManyToManyField(Other)

            class Meta:
                app_label = 'tests'

        def a_callable(obj):
            return ''

        class ThingAdmin(ModelAdmin):
            list_display = (a_callable, 'others')
        self.assertIsInvalid(ThingAdmin, Thing, "The value of 'list_display[1]' must not be a ManyToManyField.", 'admin.E109')

from django.db import models
from django.contrib.admin.checks import ModelAdminChecks
from django.contrib.admin.sites import AdminSite
from django.db import models
from django.db.models import Field, Model
from django.contrib.admin.checks import ModelAdminChecks
from django.contrib.admin.options import ModelAdmin
from .models import ValidationTestModel
from .test_checks import CheckTestCase

class ListDisplayRegressionTests(CheckTestCase):

    def test_class_level_attribute_is_valid(self):

        class Thing(Model):
            class_attr = 123

        class ThingAdmin(ModelAdmin):
            list_display = ('class_attr',)
        admin_obj = ThingAdmin(Thing, AdminSite())
        errors = ModelAdminChecks()._check_list_display(admin_obj)
        self.assertEqual(errors, [])