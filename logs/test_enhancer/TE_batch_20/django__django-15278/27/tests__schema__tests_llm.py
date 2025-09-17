from django.test import TransactionTestCase
from django.test.utils import isolate_apps, CaptureQueriesContext
from django.db import connection
from django.db import IntegrityError
from django.db.models import AutoField, BigAutoField, IntegerField, CharField, BooleanField, TextField, ForeignKey, OneToOneField, CASCADE