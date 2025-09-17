from django.db import connections
from django.test import TestCase
from django.db import connections
import re
from .models import Author, Article, OrderedByAuthorArticle, Reference