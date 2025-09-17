import inspect
from django.test import SimpleTestCase
from django.db import models
from django.db.models.manager import BaseManager
from django.db.models import QuerySet
from .models import Article