from django.db import connections
from django.db.models import Model
from django.db.utils import IntegrityError
from django.apps.registry import apps
from django.contrib.contenttypes.management import RenameContentType
from django.contrib.contenttypes.models import ContentType
from django.db import connections, transaction
from django.db.utils import IntegrityError
from django.db.models import Model
from django.test import TransactionTestCase, override_settings