import datetime
from django.core.exceptions import FieldDoesNotExist
from django.db.models import F, Value
from django.db.models.functions import Lower
from django.test import TestCase, skipUnlessDBFeature
from .models import Article, CustomDbColumn, JSONFieldNullable, Individual, Note, Number