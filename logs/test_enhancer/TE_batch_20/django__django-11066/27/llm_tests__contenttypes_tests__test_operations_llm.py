from unittest.mock import patch, Mock
from django.db import connections, IntegrityError
from django.db import migrations
from django.apps.registry import apps
from django.contrib.contenttypes import management as contenttypes_management
from django.contrib.contenttypes.models import ContentType
from django.db import connections, IntegrityError
from django.db import router
from django.db import migrations
from django.test import TransactionTestCase, override_settings
from unittest.mock import patch, Mock