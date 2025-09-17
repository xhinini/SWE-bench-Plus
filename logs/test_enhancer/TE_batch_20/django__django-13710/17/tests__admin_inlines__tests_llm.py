from django.test import RequestFactory, TestCase, override_settings
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.contrib.admin import ModelAdmin, TabularInline, StackedInline
from .admin import site as admin_site
from .models import Profile, ProfileCollection