from django.test import TestCase
from django.db import connection
from django.db import DEFAULT_DB_ALIAS
from django.db.models import F
from tests.ordering.models import Article, OrderedByAuthorArticle, OrderedByFArticle, Reference, Author