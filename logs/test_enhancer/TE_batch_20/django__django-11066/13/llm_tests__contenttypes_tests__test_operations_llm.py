from django.db import connections
from django.contrib.contenttypes.management import RenameContentType, inject_rename_contenttypes_operations, get_contenttypes_and_models, create_contenttypes
from django.apps.registry import apps
from django.conf import settings
from django.contrib.contenttypes import management as contenttypes_management
from django.contrib.contenttypes.management import RenameContentType, inject_rename_contenttypes_operations, get_contenttypes_and_models, create_contenttypes
from django.contrib.contenttypes.models import ContentType
from django.db import connections, IntegrityError
from django.db import migrations, models
from django.test import TransactionTestCase, override_settings