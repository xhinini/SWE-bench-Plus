from django.db import connection
from django.db.models import CharField, SlugField, BinaryField, Model
from django.test import TransactionTestCase, isolate_apps