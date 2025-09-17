from django.db.models.expressions import SimpleCol
from django.db.models import F, Q
from django.test import SimpleTestCase
from django.db.models.sql.query import Query
from .models import Item