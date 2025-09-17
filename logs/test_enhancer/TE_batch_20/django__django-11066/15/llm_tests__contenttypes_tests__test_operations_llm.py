from unittest import mock
from types import SimpleNamespace
from types import SimpleNamespace
import io
from unittest import mock
from django.apps.registry import apps
from django.conf import settings
from django.contrib.contenttypes import management as contenttypes_management
from django.contrib.contenttypes.models import ContentType
from django.db import IntegrityError, connections, router
from django.db import migrations
from django.test import TransactionTestCase, override_settings