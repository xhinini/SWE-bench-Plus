from django.db.models import Value
from datetime import datetime
from django.db.models import Count, Max, Value
from django.db.models.functions import Upper
from django.test import TestCase
from .models import Article, Author