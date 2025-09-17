import re
from datetime import datetime
import re
from operator import attrgetter
from django.db.models import CharField, Count, DateTimeField, F, Max, OuterRef, Subquery, Value
from django.db.models.functions import Upper
from django.test import TestCase
from .models import Article, Author, ChildArticle, OrderedByFArticle, Reference