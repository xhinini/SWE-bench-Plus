from django.db import connections
from django.apps.registry import apps
from django.contrib.contenttypes import management as contenttypes_management
from django.contrib.contenttypes.models import ContentType
from django.test import override_settings