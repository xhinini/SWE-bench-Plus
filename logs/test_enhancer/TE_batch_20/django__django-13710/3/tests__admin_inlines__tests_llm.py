from django.contrib.admin import ModelAdmin, TabularInline, StackedInline
from django.test import RequestFactory, TestCase
from django.urls import reverse
from .admin import site as admin_site
from .models import Parent, Child, ProfileCollection, Profile