from django.db import connections
from django.apps.registry import apps
from django.apps.registry import apps
from django.contrib.contenttypes.management import RenameContentType
from django.contrib.contenttypes.models import ContentType
from django.test import TransactionTestCase, override_settings
from django.db import connections
from django.db import IntegrityError
from django.db.models import Model
from unittest import mock