from django.db import connections
from django.db.models import Value
from django.test import TestCase
from django.db import connections
from django.db.models import F, Value
from .models import Note, Individual, CustomDbColumn, Order, Number