import uuid
from django.db import connection, models
from django.test import TestCase
from django.db.models import BigAutoField, UUIDField, CharField, AutoField
from django.db import transaction