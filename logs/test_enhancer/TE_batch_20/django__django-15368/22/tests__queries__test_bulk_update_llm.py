import django.db.models.query as query_mod
import copy
from django.test import TestCase, skipUnlessDBFeature
from django.db.models import F
import django.db.models.query as query_mod
from .models import Note, Number, Individual, CustomDbColumn, Tag, JSONFieldNullable
_SENTINEL = object()