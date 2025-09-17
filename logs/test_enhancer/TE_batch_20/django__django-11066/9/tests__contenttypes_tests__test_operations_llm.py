from django.apps.registry import apps
from django.conf import settings
from django.contrib.contenttypes import management as contenttypes_management
from django.contrib.contenttypes.models import ContentType
from django.db import connections, IntegrityError, router
from django.db import migrations
from django.test import TransactionTestCase, override_settings
from django.db import DEFAULT_DB_ALIAS