from unittest import mock
from django.db import connections, IntegrityError, router
from unittest import mock
from django.apps.registry import apps
from django.contrib.contenttypes import management as contenttypes_management
from django.contrib.contenttypes.models import ContentType
from django.db import IntegrityError, connections
from django.test import TransactionTestCase, override_settings