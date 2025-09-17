import itertools
import itertools
from django import forms
from django.test import TestCase
from django.core.exceptions import ValidationError
from django.forms.models import ModelChoiceIteratorValue, ModelChoiceIterator
from .models import Category