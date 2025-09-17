from django.test import TestCase
from django.db.models import F, Value
from django.db.models.functions import Lower
from django.db import transaction
from .models import Note, Number, Individual