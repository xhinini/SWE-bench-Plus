from datetime import datetime
from django.db.models import CharField, Count, DateTimeField, F, Max, OuterRef, Subquery, Value
from django.db.models.functions import Upper
from django.test import TestCase
from .models import Article, Author