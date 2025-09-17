import datetime
from django.db.models import F, Value
from django.db.models.functions import Lower
import datetime
from django.test import TestCase, override_settings
from django.db.models import F, Value
from django.db.models.functions import Lower
from tests.queries.models import Note, Number, Individual, CustomDbColumn, Article