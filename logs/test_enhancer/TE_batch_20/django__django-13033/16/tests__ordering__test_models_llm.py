from django.test import TestCase
from django.db import connection
from django.db.models import F, OrderBy
from django.db.models.constants import LOOKUP_SEP
from django.db import connections
from tests.ordering.models import Author, Article, OrderedByAuthorArticle, OrderedByFArticle, Reference