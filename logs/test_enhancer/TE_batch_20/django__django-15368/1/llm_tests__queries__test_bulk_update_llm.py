import datetime
from django.test import TestCase, skipUnlessDBFeature
from django.db.models import F, Value
from django.db.models.functions import Lower
from .models import Note, Number, Individual, JSONFieldNullable, Tag