import re
from django.test import SimpleTestCase
from django.db import connection
from tests.ordering.models import Article, Reference, Author