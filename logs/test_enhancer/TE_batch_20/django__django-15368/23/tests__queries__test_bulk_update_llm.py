from django.db.models import F, Value
from django.db.models.functions import Lower
from django.test import TestCase
from .models import Number, Note, Individual