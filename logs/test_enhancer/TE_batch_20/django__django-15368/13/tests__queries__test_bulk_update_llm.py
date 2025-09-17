from django.db.models import Value, F
from django.db.models.functions import Lower
from django.test import TestCase, skipUnlessDBFeature
from django.db.models import F, Value
from django.db.models.functions import Lower
import datetime
from .models import Note, Number, Individual, CustomDbColumn, Article, JSONFieldNullable