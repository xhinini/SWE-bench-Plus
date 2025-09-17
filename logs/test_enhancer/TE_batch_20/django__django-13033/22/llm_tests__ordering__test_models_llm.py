from django.test import TestCase
from django.db import DEFAULT_DB_ALIAS
from django.db.models import F, OrderBy
from tests.ordering.models import Author, Article, OrderedByAuthorArticle, OrderedByFArticle
from django.test import TestCase
from django.db import DEFAULT_DB_ALIAS
from django.db import connection
from django.db.models import F, OrderBy
from tests.ordering.models import Author, Article, OrderedByAuthorArticle, OrderedByFArticle