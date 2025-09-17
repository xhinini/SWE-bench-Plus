import inspect
from unittest import mock
from django.test import SimpleTestCase
from django.db import models as django_models
from .models import Article