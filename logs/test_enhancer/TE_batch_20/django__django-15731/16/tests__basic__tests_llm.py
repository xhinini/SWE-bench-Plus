from django.test import SimpleTestCase
import inspect
from django.db import models
from .models import Article
from django.db.models.manager import BaseManager, Manager