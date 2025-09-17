from django.test import TestCase
from django.db.models import F, Value
from django.db.models.functions import Lower
from .models import Number, Note, Order