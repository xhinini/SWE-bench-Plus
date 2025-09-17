from django.utils.text import format_lazy, capfirst
from django.test import RequestFactory, TestCase, override_settings
from django.utils.text import format_lazy, capfirst
from .admin import site as admin_site
from .models import Child, Person, Parent
from django.contrib.admin import TabularInline, StackedInline, ModelAdmin