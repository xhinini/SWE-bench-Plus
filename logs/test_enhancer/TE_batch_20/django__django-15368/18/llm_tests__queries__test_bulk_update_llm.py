from django.db.models import Value
from django.utils import timezone
from django.test import TestCase, skipUnlessDBFeature
from django.db.models import F, Value
from django.db.models.functions import Lower
from django.utils import timezone
import datetime
from .models import Number, Note, Individual, CustomDbColumn, Article, JSONFieldNullable, Order