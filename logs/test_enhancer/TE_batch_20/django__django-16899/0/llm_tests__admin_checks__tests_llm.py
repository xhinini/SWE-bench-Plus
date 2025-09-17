from django.contrib import admin
from django.contrib.admin import AdminSite
from django.core import checks
from django.test import SimpleTestCase, override_settings
from .models import Song, City