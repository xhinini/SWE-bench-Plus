from django.test import SimpleTestCase
from django.forms.formsets import formset_factory, BaseFormSet
from django.forms import Form, CharField, IntegerField
from django.forms.renderers import get_default_renderer
try:
    Choice
except NameError: