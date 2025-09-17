from django.test import SimpleTestCase
import inspect
from django.db import models
from django.db.models.manager import BaseManager
from django.db.models.query import QuerySet
from .models import Article