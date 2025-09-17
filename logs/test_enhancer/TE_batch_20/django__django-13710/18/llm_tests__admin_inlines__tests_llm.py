from django.contrib.admin import ModelAdmin, TabularInline, StackedInline
from django.test import TestCase
from .admin import site as admin_site
from .models import Child, Person, ProfileCollection, Profile, VerboseNameProfile