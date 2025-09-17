import datetime
import unittest
from django.db import connection
from django.db.models import IntegerField, CharField, BinaryField, BooleanField, TextField, DurationField, DateField, TimeField, DecimalField, FloatField
from django.test import skipUnlessDBFeature