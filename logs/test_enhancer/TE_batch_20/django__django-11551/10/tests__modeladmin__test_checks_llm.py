from django.db import models
from django.contrib.admin.options import ModelAdmin
from django.db.models import Model, Field
from django.test import SimpleTestCase
from django.contrib.admin.options import ModelAdmin
from django.contrib.admin.sites import AdminSite
from django.contrib.admin.checks import ModelAdminChecks
from django.core.checks import Error
from .models import ValidationTestModel