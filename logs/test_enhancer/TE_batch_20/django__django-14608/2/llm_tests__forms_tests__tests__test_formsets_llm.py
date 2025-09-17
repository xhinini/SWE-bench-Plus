from django.forms.utils import ErrorList
from django.test import SimpleTestCase
try:
    ChoiceFormSet
except NameError:
    ChoiceFormSet = None

class NonFormErrorsRegressionTests(SimpleTestCase):

    def setUp(self):
        self.valid_data = {'choices-TOTAL_FORMS': '1', 'choices-INITIAL_FORMS': '0', 'choices-MIN_NUM_FORMS': '0', 'choices-MAX_NUM_FORMS': '0', 'choices-0-choice': 'Zero', 'choices-0-votes': '0'}

from django.forms.formsets import formset_factory, BaseFormSet
from django.forms import Form, CharField, IntegerField, ValidationError
from django.forms.utils import ErrorList
from django.test import SimpleTestCase
from django.forms.formsets import formset_factory, BaseFormSet
from django.forms import Form, CharField, IntegerField, ValidationError
ChoiceFormSet = formset_factory(Choice)

class NonFormErrorsRegressionTests(SimpleTestCase):

    def make_valid_choice_formset(self):
        data = {'choices-TOTAL_FORMS': '1', 'choices-INITIAL_FORMS': '0', 'choices-MIN_NUM_FORMS': '0', 'choices-MAX_NUM_FORMS': '0', 'choices-0-choice': 'Zero', 'choices-0-votes': '1'}
        return ChoiceFormSet(data, auto_id=False, prefix='choices')