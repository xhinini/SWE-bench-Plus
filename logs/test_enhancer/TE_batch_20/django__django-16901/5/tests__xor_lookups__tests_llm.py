from types import SimpleNamespace
from types import SimpleNamespace
from django.test import SimpleTestCase
from django.db.models import Q
from django.db.models.functions import Mod
from django.db.models.lookups import Exact
from django.db.models.sql.where import WhereNode, XOR, OR, AND