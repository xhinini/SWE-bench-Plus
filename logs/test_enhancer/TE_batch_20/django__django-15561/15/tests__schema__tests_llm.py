from copy import copy
from django.db import connection
from django.db.models import CharField, IntegerField, TextField, BinaryField, DecimalField, DateField, DateTimeField, DurationField, UUIDField, SlugField, Model
from django.test import TestCase, isolate_apps