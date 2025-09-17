from django.db import connections, router
from unittest.mock import patch
from django.apps.registry import apps
from django.contrib.contenttypes.management import RenameContentType
from django.contrib.contenttypes.models import ContentType
from django.test import TransactionTestCase
from django.db import connections, router
from unittest.mock import patch