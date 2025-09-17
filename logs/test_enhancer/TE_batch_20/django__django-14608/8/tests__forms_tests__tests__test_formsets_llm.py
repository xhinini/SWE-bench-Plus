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

# No new imports required; tests reuse objects defined in the module under test.
from django.forms.formsets import formset_factory
from django.test import SimpleTestCase
from django.forms import CharField, Form, IntegerField
from django.forms.utils import ErrorList

# Reuse Choice and ChoiceFormSet from the module under test (defined in the existing tests).
# If not available, define a minimal Choice here to ensure these tests are self-contained.
try:
    Choice  # noqa: F821
    ChoiceFormSet  # noqa: F821
except NameError:
    class Choice(Form):
        choice = CharField()
        votes = IntegerField()
    ChoiceFormSet = formset_factory(Choice)

class NonFormErrorsIdentityTests(SimpleTestCase):
    def _make_empty_bound_formset(self, extra=1):
        # A formset bound with no forms (TOTAL_FORMS == 0) but marked bound
        FS = formset_factory(Choice, extra=extra)
        data = {
            'choices-TOTAL_FORMS': '0',
            'choices-INITIAL_FORMS': '0',
            'choices-MIN_NUM_FORMS': '0',
            'choices-MAX_NUM_FORMS': '0',
        }
        return FS(data, auto_id=False, prefix='choices')

    def test_unbound_full_clean_then_non_form_errors_is_stored(self):
        formset = ChoiceFormSet()
        # force full_clean to populate _non_form_errors
        formset.full_clean()
        nf = formset.non_form_errors()
        # The returned ErrorList must be the same object stored on the formset
        self.assertIs(nf, formset._non_form_errors)

    def test_bound_full_clean_then_non_form_errors_is_stored(self):
        formset = self._make_empty_bound_formset()
        # full_clean already run by management of non_form_errors in some code paths,
        # but ensure it is present
        formset.full_clean()
        nf = formset.non_form_errors()
        self.assertIs(nf, formset._non_form_errors)

    def test_non_form_errors_first_call_triggers_full_clean_and_returns_stored(self):
        formset = self._make_empty_bound_formset()
        # don't call full_clean explicitly; non_form_errors() should call it and
        # return the stored ErrorList instance (not a newly constructed one)
        nf = formset.non_form_errors()
        self.assertIs(nf, formset._non_form_errors)

    def test_multiple_non_form_errors_calls_return_same_object(self):
        formset = self._make_empty_bound_formset()
        first = formset.non_form_errors()
        second = formset.non_form_errors()
        self.assertIs(first, second)
        self.assertIs(second, formset._non_form_errors)

    def test_mutating_returned_non_form_errors_updates_stored(self):
        formset = self._make_empty_bound_formset()
        nf = formset.non_form_errors()
        # mutate the returned ErrorList
        nf.append('mutated-error')
        # mutations must be visible on the stored object
        self.assertIn('mutated-error', list(formset._non_form_errors))

    def test_mutating_after_is_valid_updates_stored(self):
        formset = self._make_empty_bound_formset()
        # call is_valid which triggers full_clean; there are no non-form errors here
        self.assertTrue(formset.is_bound)
        _ = formset.is_valid()
        nf = formset.non_form_errors()
        nf.append('after-is-valid')
        self.assertIn('after-is-valid', list(formset._non_form_errors))

    def test_non_form_errors_identity_with_extra_zero(self):
        FS = formset_factory(Choice, extra=0)
        data = {
            'choices-TOTAL_FORMS': '0',
            'choices-INITIAL_FORMS': '0',
        }
        formset = FS(data, prefix='choices')
        # ensure full_clean executed via non_form_errors()
        nf = formset.non_form_errors()
        self.assertIs(nf, formset._non_form_errors)

    def test_non_form_errors_identity_loop_multiple_calls(self):
        formset = ChoiceFormSet()
        formset.full_clean()
        refs = [formset.non_form_errors() for _ in range(5)]
        # all returned references should be the same object
        for ref in refs:
            self.assertIs(ref, formset._non_form_errors)

    def test_non_form_errors_append_then_str_reflects(self):
        formset = self._make_empty_bound_formset()
        nf = formset.non_form_errors()
        nf.append('visible-message')
        # The string rendering must include the appended message
        rendered = str(formset.non_form_errors())
        self.assertIn('visible-message', rendered)

    def test_non_form_errors_is_errorlist_instance_and_is_stored(self):
        formset = ChoiceFormSet()
        formset.full_clean()
        nf = formset.non_form_errors()
        self.assertIsInstance(nf, ErrorList)
        self.assertIs(nf, formset._non_form_errors)

from django.forms.utils import ErrorList
from django.test import SimpleTestCase

class NonFormErrorsRegressionTests(SimpleTestCase):

    def make_choice_data(self, total=1, initial=0, choice='X', votes='1'):
        return {'choices-TOTAL_FORMS': str(total), 'choices-INITIAL_FORMS': str(initial), 'choices-MIN_NUM_FORMS': '0', 'choices-MAX_NUM_FORMS': '0', 'choices-0-choice': choice, 'choices-0-votes': votes}