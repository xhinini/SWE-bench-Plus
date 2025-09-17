from django.contrib.admin.options import ModelAdmin
from django.test import SimpleTestCase
from django.db.models import Model, Field
from django.core.checks import Error
from .test_checks import CheckTestCase
from .models import ValidationTestModel