from django.test import override_settings, TestCase, RequestFactory
from django.contrib.admin import ModelAdmin, TabularInline, StackedInline
from django.utils.text import format_lazy
from .admin import site as admin_site
from .models import Child, Parent, Teacher