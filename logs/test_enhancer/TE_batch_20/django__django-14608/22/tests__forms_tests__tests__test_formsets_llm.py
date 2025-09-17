from django.core.exceptions import ValidationError
from django.forms import Form, CharField, IntegerField
from django.forms.formsets import BaseFormSet, formset_factory
from django.forms.utils import ErrorList
from django.test import SimpleTestCase
ChoiceFormSet = formset_factory(Choice)