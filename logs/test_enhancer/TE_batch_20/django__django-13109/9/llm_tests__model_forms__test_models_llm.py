from django.test import TestCase
from django.core.exceptions import ValidationError
import datetime
from tests.model_forms.models import Writer, Article, WriterProfile, Book