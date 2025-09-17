from django.contrib.admin.options import ModelAdmin
from django.contrib.admin.sites import AdminSite
from django.core.checks import Error
from django.db.models import Field, Model, CharField, IntegerField, ManyToManyField
from django.test import SimpleTestCase
from .models import ValidationTestModel