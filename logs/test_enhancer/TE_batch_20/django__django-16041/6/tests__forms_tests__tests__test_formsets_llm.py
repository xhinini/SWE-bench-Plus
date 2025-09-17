from django.test import SimpleTestCase
from django.forms.formsets import formset_factory
from django.forms import Form, CharField, IntegerField
SimpleFormSet = formset_factory(SimpleForm)