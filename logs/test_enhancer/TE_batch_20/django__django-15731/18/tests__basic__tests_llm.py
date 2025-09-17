import inspect
from types import SimpleNamespace
from django.test import SimpleTestCase
from django.db import models
from django.db.models.manager import BaseManager
from .models import Article