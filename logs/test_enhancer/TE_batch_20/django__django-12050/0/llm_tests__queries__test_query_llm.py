from django.db.models import Value
from django.db.models import F, Value
from django.db.models.expressions import SimpleCol
from django.db.models.sql.query import Query
from django.db.models import Q
from django.test import SimpleTestCase
from .models import Author, Item