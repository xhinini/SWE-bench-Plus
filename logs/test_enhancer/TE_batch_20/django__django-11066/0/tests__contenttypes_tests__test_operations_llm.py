from django.apps.registry import apps
from django.db import connections
from unittest import mock
from django.db.utils import IntegrityError
from django.contrib.contenttypes import management as contenttypes_management
from django.contrib.contenttypes.models import ContentType
from django.db import migrations
from django.test import TransactionTestCase