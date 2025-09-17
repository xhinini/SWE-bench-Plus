from django.contrib.admin import ModelAdmin, TabularInline, StackedInline
from django.urls import reverse
from django.test import RequestFactory, TestCase, override_settings
from django.contrib.admin import ModelAdmin
from django.contrib.admin import TabularInline, StackedInline
from .admin import site as admin_site
from .models import ProfileCollection, Profile
from django.contrib.auth.models import User