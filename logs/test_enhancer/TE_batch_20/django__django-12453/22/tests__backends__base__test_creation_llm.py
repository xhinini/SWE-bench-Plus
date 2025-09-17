from unittest import mock
from io import StringIO
from django.test import SimpleTestCase
from django.db import connection
from django.core import serializers
import django.db.backends.base.creation as creation_module