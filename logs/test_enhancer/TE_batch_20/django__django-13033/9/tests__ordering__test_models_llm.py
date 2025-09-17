from django.test import TestCase
from django.db import connections
from .models import Author, Article, OrderedByAuthorArticle, OrderedByFArticle, Reference