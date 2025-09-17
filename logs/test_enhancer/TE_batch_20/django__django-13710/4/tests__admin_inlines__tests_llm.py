from django.test import TestCase, override_settings
from django.contrib.admin import TabularInline, StackedInline
from .admin import site as admin_site
from .models import Child, Person, Teacher, Parent, ParentModelWithCustomPk, SomeParentModel, ProfileCollection