from unittest import mock
from unittest import mock
from django.apps.registry import apps
from django.conf import settings
from django.contrib.contenttypes import management as contenttypes_management
from django.contrib.contenttypes.models import ContentType
from django.db import IntegrityError, connections
from django.test import TransactionTestCase, override_settings