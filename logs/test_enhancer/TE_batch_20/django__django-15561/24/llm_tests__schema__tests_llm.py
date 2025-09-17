from copy import copy
from django.db import connection
from django.db.models import BooleanField, CharField, DateField, DecimalField, DurationField, FloatField, IntegerField, Model, TimeField, UUIDField
from django.test import TransactionTestCase, isolate_apps