from django.test import SimpleTestCase
from django.core.validators import MaxLengthValidator
from django.core.exceptions import ValidationError
from django.db.models import CharField, TextField, BinaryField