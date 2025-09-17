from django.db.models import Count, Max, Value
from django.db.models.functions import Upper
from datetime import datetime
from operator import attrgetter
from django.db.models import Count, Max, Value
from django.db.models.functions import Upper
from django.test import TestCase
from .models import Article, Author, ChildArticle, OrderedByFArticle