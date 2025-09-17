from django.test import TestCase
from .admin import site as admin_site
from .models import Child, Person, SomeChildModel, Profile, FootNote, ParentModelWithCustomPk, SomeParentModel, Novel, Book, Inner, Chapter
from django.contrib.admin import TabularInline