from django.test import TestCase, skipUnlessDBFeature
from django.db.models import F, Value, Case, When, Cast, IntegerField, Lower
from .models import Note, Number, Individual, Article, JSONFieldNullable, CustomDbColumn