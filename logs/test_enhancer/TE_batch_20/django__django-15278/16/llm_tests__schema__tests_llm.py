from django.db import connection
from django.db.models import AutoField, BigAutoField, CharField, IntegerField, Model
from django.test.utils import isolate_apps
import unittest
from django.test import skipUnlessDBFeature