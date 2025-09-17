from unittest import mock
import uuid
from django.db.models.query import QuerySet
from django.test import TestCase
from django.db import DEFAULT_DB_ALIAS
from tests.serializers.models.data import UUIDDefaultData, BooleanPKData