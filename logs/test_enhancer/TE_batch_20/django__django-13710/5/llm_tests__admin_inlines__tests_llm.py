from django.utils.safestring import mark_safe
from django.contrib.admin import ModelAdmin, TabularInline, StackedInline
from django.test import RequestFactory, override_settings, TestCase