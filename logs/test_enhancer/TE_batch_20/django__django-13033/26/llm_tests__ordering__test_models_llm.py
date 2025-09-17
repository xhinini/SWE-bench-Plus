from django.test import TestCase
from django.db.models import F, OrderBy
from django.core.exceptions import FieldError
from django.db import connection
from tests.ordering.models import Author, Article, Reference, OrderedByAuthorArticle