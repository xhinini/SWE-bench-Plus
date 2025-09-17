from django.db import connection
from django.db.models import CharField, ForeignKey, Model, CASCADE
from django.test import TransactionTestCase, isolate_apps
from django.test.utils import CaptureQueriesContext