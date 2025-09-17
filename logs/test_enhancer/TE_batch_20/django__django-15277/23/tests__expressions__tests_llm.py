from copy import deepcopy
from django import forms
from django.core.validators import MaxLengthValidator
from django.test import SimpleTestCase
from django.core import validators
from django.db.models import CharField