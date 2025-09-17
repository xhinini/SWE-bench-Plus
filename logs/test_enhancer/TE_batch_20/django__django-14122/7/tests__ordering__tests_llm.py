from django.db import connection
from datetime import datetime
from operator import attrgetter
from django.db import connection
from django.db.models import Count, DateTimeField, F, Max, OuterRef, Subquery, Value
from django.db.models.functions import Upper
from django.test import TestCase
from .models import Article, Author, ChildArticle, OrderedByFArticle, Reference