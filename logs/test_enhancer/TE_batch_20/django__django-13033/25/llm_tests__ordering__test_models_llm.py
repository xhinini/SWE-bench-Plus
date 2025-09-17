from django.db.models.sql.query import Query
from django.db.models.sql.compiler import SQLCompiler
from django.test import TestCase
from django.db import connection
from django.db.models.sql.query import Query
from django.db.models.sql.compiler import SQLCompiler
from tests.ordering.models import Author, Article
import re