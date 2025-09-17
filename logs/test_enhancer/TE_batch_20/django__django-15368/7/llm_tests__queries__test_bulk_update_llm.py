from django.test import TestCase, skipUnlessDBFeature
from django.db.models import F, Value
from django.utils import timezone
import datetime
from .models import Note, Number, Individual, CustomDbColumn, Article, JSONFieldNullable, Tag