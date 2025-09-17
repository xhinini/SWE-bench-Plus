from django.test import TestCase
from django.db import connection
from django.db import reset_queries
from django.conf import settings
from django.apps import apps
from django.db import migrations, models as djmodels
from tests.ordering.models import Author, Article