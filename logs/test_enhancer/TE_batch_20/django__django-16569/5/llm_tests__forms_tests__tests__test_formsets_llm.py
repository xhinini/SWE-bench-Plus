from django.forms import Form, CharField, IntegerField
from django.forms.widgets import HiddenInput
from django.test import SimpleTestCase
from django.forms.formsets import BaseFormSet, formset_factory
try:
    Choice
except NameError: