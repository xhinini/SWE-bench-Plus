from datetime import datetime
from django.db.models import CharField, Count, Max, Value, F
from django.db.models.functions import Upper
from django.test import TestCase
from .models import Article, Author