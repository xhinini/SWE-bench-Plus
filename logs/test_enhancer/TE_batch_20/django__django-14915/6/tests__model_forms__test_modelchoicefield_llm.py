from django.forms.models import ModelChoiceIteratorValue, ModelChoiceIterator, ModelChoiceField
import copy
from django.test import TestCase
from django.core.exceptions import ValidationError
from django.forms.models import ModelChoiceIteratorValue, ModelChoiceIterator, ModelChoiceField
from django.template import Context, Template
from .models import Category