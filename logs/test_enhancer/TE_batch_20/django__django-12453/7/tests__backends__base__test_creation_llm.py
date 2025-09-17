from contextlib import contextmanager
from contextlib import contextmanager
from unittest import mock
from django.core import serializers
from django.db import connection
from django.test import SimpleTestCase
from ..models import Object, ObjectReference
from ..test_creation import get_connection_copy