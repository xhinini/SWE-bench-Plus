from django.test import SimpleTestCase
from django.core.exceptions import ValidationError
from django.core.validators import MaxLengthValidator
from django import forms
from django.db.models import CharField