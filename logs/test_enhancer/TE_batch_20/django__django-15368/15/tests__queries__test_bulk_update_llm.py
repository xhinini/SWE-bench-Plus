from django.test import TestCase
from django.db.models import F, Value
from django.db import transaction
from .models import Note, Number, CustomDbColumn, Individual