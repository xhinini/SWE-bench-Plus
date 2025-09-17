from django.db.models import Value, F
from django.apps import apps
from collections import namedtuple
from typing import NamedTuple as TypingNamedTuple
from django.test import TestCase
from django.db.models import Value, F
from django.db.models.sql.query import Query
from django.apps import apps
Company = apps.get_model('expressions', 'Company')