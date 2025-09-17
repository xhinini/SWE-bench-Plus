import uuid
from django.db import connection, models
from django.test import TestCase
from django.db.models.deletion import Collector
from tests.delete.tests import User