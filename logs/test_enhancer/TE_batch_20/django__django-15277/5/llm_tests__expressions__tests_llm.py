from django.test import SimpleTestCase
from django.core.validators import MaxLengthValidator
from django.core.exceptions import ValidationError
from django.db.models import CharField, TextField, SlugField, EmailField, Value
from django.db.models.fields import BLANK_CHOICE_DASH