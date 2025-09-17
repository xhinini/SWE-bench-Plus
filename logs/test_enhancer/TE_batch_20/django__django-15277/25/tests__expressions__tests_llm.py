from django.test import SimpleTestCase
from django.db.models import CharField, Value
from django.core.validators import MaxLengthValidator
from django.core.exceptions import ValidationError