from django.db.models import Value
import datetime
from django.test import TestCase, skipUnlessDBFeature
from django.db.models import F, Value, Lower
from .models import Number, Note, Individual, Tag, Article, JSONFieldNullable, Order