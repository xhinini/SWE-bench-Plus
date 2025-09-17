from unittest import SkipTest
from unittest import SkipTest
from django.contrib.admin import ModelAdmin, TabularInline
from django.test import RequestFactory, TestCase, override_settings
from django.urls import reverse
from .admin import site as admin_site
from .models import Profile, VerboseNameProfile, VerboseNamePluralProfile, BothVerboseNameProfile, ProfileCollection