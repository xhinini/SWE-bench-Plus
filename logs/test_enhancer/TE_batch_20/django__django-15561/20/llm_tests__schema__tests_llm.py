from django.db import connection
from django.db.models import CharField, TextField, SlugField, IntegerField, DateField, Model
from django.test import TransactionTestCase, isolate_apps
from django.test.utils import CaptureQueriesContext