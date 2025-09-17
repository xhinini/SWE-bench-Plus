from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import MaxLengthValidator
from django.test import SimpleTestCase
from django.db.models import CharField, SlugField