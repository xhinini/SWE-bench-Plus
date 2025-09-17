from django.test import TestCase
from django.db import connection
from django.db import connections
from django.db import DEFAULT_DB_ALIAS
from .models import Author, Article