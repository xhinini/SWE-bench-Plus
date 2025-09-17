from django.db import DEFAULT_DB_ALIAS
from django.test import TestCase
from django.db import DatabaseError, DEFAULT_DB_ALIAS
import uuid
from tests.serializers.models.data import UUIDDefaultData, BooleanPKData