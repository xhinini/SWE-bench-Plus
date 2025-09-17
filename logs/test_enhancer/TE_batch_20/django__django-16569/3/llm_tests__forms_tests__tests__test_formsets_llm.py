from django.forms import Form, FileField
from django.forms.widgets import HiddenInput
from django.test import SimpleTestCase
from django.forms.formsets import BaseFormSet, formset_factory
from .test_formsets import Choice