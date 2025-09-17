from django.db.models import F, Value
from django.db.models.functions import Lower
from django.test import TestCase
from django.db import transaction
from django.db.models import F, Value
from django.db.models.functions import Lower
from .models import Note, Number, CustomDbColumn, Order, CustomPk