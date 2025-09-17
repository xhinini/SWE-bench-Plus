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