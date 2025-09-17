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

# No new module-level imports required beyond those in the test code.
from django.forms import Form, CharField, IntegerField
from django.forms.formsets import formset_factory, all_valid
from django.test import SimpleTestCase


class SimpleForm(Form):
    name = CharField()
    value = IntegerField(required=False)


class NonFormErrorsIdentityTests(SimpleTestCase):

    def test_non_form_errors_returns_internal_instance_on_valid_formset(self):
        FormSet = formset_factory(SimpleForm)
        data = {
            'form-TOTAL_FORMS': '1',
            'form-INITIAL_FORMS': '0',
            'form-MIN_NUM_FORMS': '0',
            'form-MAX_NUM_FORMS': '0',
            'form-0-name': 'Alice',
            'form-0-value': '10',
        }
        formset = FormSet(data, prefix='form')
        # Ensure it's valid and there are no non-form errors
        self.assertTrue(formset.is_valid())
        nf = formset.non_form_errors()
        # The returned object should be the same object as the internal attribute
        self.assertIs(nf, formset._non_form_errors)
        # Repeated calls should return the same object
        self.assertIs(formset.non_form_errors(), nf)

    def test_non_form_errors_identity_after_manual_full_clean(self):
        FormSet = formset_factory(SimpleForm)
        data = {
            'form-TOTAL_FORMS': '1',
            'form-INITIAL_FORMS': '0',
            'form-0-name': 'Bob',
            'form-0-value': '5',
        }
        formset = FormSet(data, prefix='form')
        # Call full_clean manually, then non_form_errors should return the same instance
        formset.full_clean()
        nf = formset.non_form_errors()
        self.assertIs(nf, formset._non_form_errors)

    def test_non_form_errors_identity_on_empty_formset_with_zero_forms(self):
        FormSet = formset_factory(SimpleForm, extra=0)
        data = {
            'form-TOTAL_FORMS': '0',
            'form-INITIAL_FORMS': '0',
            'form-MIN_NUM_FORMS': '0',
            'form-MAX_NUM_FORMS': '0',
        }
        formset = FormSet(data, prefix='form')
        # Bound, no non-form errors expected
        nf = formset.non_form_errors()
        self.assertIs(nf, formset._non_form_errors)
        # Empty ErrorList should still be the same object across calls
        self.assertIs(formset.non_form_errors(), nf)

    def test_non_form_errors_identity_with_can_delete(self):
        FormSet = formset_factory(SimpleForm, can_delete=True)
        data = {
            'form-TOTAL_FORMS': '1',
            'form-INITIAL_FORMS': '0',
            'form-MIN_NUM_FORMS': '0',
            'form-MAX_NUM_FORMS': '0',
            'form-0-name': 'Carol',
            'form-0-value': '7',
            'form-0-DELETE': '',
        }
        formset = FormSet(data, prefix='form')
        self.assertTrue(formset.is_valid())
        nf = formset.non_form_errors()
        self.assertIs(nf, formset._non_form_errors)

    def test_non_form_errors_identity_with_can_order(self):
        FormSet = formset_factory(SimpleForm, can_order=True)
        data = {
            'form-TOTAL_FORMS': '1',
            'form-INITIAL_FORMS': '0',
            'form-MIN_NUM_FORMS': '0',
            'form-MAX_NUM_FORMS': '0',
            'form-0-name': 'Dave',
            'form-0-value': '3',
            'form-0-ORDER': '1',
        }
        formset = FormSet(data, prefix='form')
        self.assertTrue(formset.is_valid())
        nf = formset.non_form_errors()
        self.assertIs(nf, formset._non_form_errors)

    def test_non_form_errors_mutation_is_reflected_on_formset_internal(self):
        FormSet = formset_factory(SimpleForm)
        data = {
            'form-TOTAL_FORMS': '1',
            'form-INITIAL_FORMS': '0',
            'form-0-name': 'Eve',
            'form-0-value': '2',
        }
        formset = FormSet(data, prefix='form')
        self.assertTrue(formset.is_valid())
        nf = formset.non_form_errors()
        # Mutate the returned ErrorList
        nf.append('injected-error')
        # The formset internal _non_form_errors should reflect the mutation
        self.assertIn('injected-error', formset._non_form_errors)

    def test_non_form_errors_mutation_persists_across_calls(self):
        FormSet = formset_factory(SimpleForm)
        data = {
            'form-TOTAL_FORMS': '1',
            'form-INITIAL_FORMS': '0',
            'form-0-name': 'Frank',
            'form-0-value': '9',
        }
        formset = FormSet(data, prefix='form')
        self.assertTrue(formset.is_valid())
        first = formset.non_form_errors()
        first.append('persisted-error')
        # Subsequent calls should return the same object and include the mutation
        second = formset.non_form_errors()
        self.assertIs(first, second)
        self.assertIn('persisted-error', second)

    def test_non_form_errors_identity_after_all_valid_call(self):
        FormSet = formset_factory(SimpleForm)
        data = {
            'form-TOTAL_FORMS': '1',
            'form-INITIAL_FORMS': '0',
            'form-0-name': 'Gina',
            'form-0-value': '4',
        }
        fs1 = FormSet(data, prefix='form')
        fs2 = FormSet(data, prefix='form')
        # all_valid will call is_valid() on all formsets; afterwards non_form_errors should be stable
        self.assertTrue(all_valid((fs1, fs2)))
        nf1 = fs1.non_form_errors()
        nf2 = fs2.non_form_errors()
        self.assertIs(nf1, fs1._non_form_errors)
        self.assertIs(nf2, fs2._non_form_errors)

    def test_non_form_errors_str_and_identity(self):
        FormSet = formset_factory(SimpleForm)
        data = {
            'form-TOTAL_FORMS': '1',
            'form-INITIAL_FORMS': '0',
            'form-0-name': 'Hank',
            'form-0-value': '11',
        }
        formset = FormSet(data, prefix='form')
        self.assertTrue(formset.is_valid())
        nf = formset.non_form_errors()
        # Converting to str should not change the identity of the underlying ErrorList
        _ = str(nf)
        self.assertIs(nf, formset._non_form_errors)

    def test_non_form_errors_mutation_after_str_call_still_persists(self):
        FormSet = formset_factory(SimpleForm)
        data = {
            'form-TOTAL_FORMS': '1',
            'form-INITIAL_FORMS': '0',
            'form-0-name': 'Ivy',
            'form-0-value': '6',
        }
        formset = FormSet(data, prefix='form')
        self.assertTrue(formset.is_valid())
        nf = formset.non_form_errors()
        _ = str(nf)
        nf.append('after-str')
        # The appended value should be visible on the internal attribute
        self.assertIn('after-str', formset._non_form_errors)

from django.forms.utils import ErrorList
from django.forms.utils import ErrorList
from django.test import SimpleTestCase
from django.forms.formsets import formset_factory, BaseFormSet
from django.forms import Form, CharField, IntegerField
from django.forms.utils import ErrorList
ChoiceFormSet = formset_factory(SimpleChoice)

class NonFormErrorsRegressionTests(SimpleTestCase):

    def make_choice(self, data=None, prefix='choices'):
        kwargs = {'auto_id': False, 'prefix': prefix}
        if data is None:
            return ChoiceFormSet(**kwargs)
        return ChoiceFormSet(data, **kwargs)

from django.test import SimpleTestCase
from django.forms.formsets import formset_factory
from django.forms.utils import ErrorList
from django.forms import Form, CharField, IntegerField
from django.forms.formsets import BaseFormSet
from django.forms.formsets import TOTAL_FORM_COUNT, INITIAL_FORM_COUNT, MIN_NUM_FORM_COUNT, MAX_NUM_FORM_COUNT
ChoiceFormSet = formset_factory(Choice)

class RegressionNonFormErrorsTests(SimpleTestCase):

    def _valid_choice_data(self, prefix='choices'):
        return {f'{prefix}-TOTAL_FORMS': '1', f'{prefix}-INITIAL_FORMS': '0', f'{prefix}-MIN_NUM_FORMS': '0', f'{prefix}-MAX_NUM_FORMS': '0', f'{prefix}-0-choice': 'Calexico', f'{prefix}-0-votes': '100'}

from django.test import SimpleTestCase
from django.forms.formsets import BaseFormSet, formset_factory
from django.forms import Form, CharField, IntegerField, ValidationError
from django.forms.formsets import all_valid
from django.forms.utils import ErrorList
from django.forms.formsets import TOTAL_FORM_COUNT, INITIAL_FORM_COUNT, MIN_NUM_FORM_COUNT, MAX_NUM_FORM_COUNT
ChoiceFormSet = formset_factory(Choice)

class NonFormErrorsRegressionTests(SimpleTestCase):

    def _valid_choice_data(self, prefix='choices'):
        return {f'{prefix}-TOTAL_FORMS': '1', f'{prefix}-INITIAL_FORMS': '0', f'{prefix}-MIN_NUM_FORMS': '0', f'{prefix}-MAX_NUM_FORMS': '0', f'{prefix}-0-choice': 'Calexico', f'{prefix}-0-votes': '100'}

    def test_non_form_errors_returns_internal_object_and_is_mutable(self):
        data = self._valid_choice_data()
        fs = ChoiceFormSet(data, auto_id=False, prefix='choices')
        nf = fs.non_form_errors()
        self.assertIs(nf, fs._non_form_errors)
        nf.append('boom')
        self.assertEqual(list(fs._non_form_errors), ['boom'])

    def test_non_form_errors_identity_after_explicit_full_clean(self):
        data = self._valid_choice_data()
        fs = ChoiceFormSet(data, auto_id=False, prefix='choices')
        fs.full_clean()
        nf = fs.non_form_errors()
        self.assertIs(nf, fs._non_form_errors)

    def test_non_form_errors_is_same_object_across_calls(self):
        data = self._valid_choice_data()
        fs = ChoiceFormSet(data, auto_id=False, prefix='choices')
        nf1 = fs.non_form_errors()
        nf2 = fs.non_form_errors()
        self.assertIs(nf1, nf2)

    def test_modifying_non_form_errors_affects_total_error_count(self):
        data = self._valid_choice_data()
        fs = ChoiceFormSet(data, auto_id=False, prefix='choices')
        nf = fs.non_form_errors()
        self.assertEqual(fs.total_error_count(), 0)
        nf.append('non-form-error')
        self.assertEqual(fs.total_error_count(), 1)

    def test_non_form_errors_mutation_persists_across_calls(self):
        data = self._valid_choice_data()
        fs = ChoiceFormSet(data, auto_id=False, prefix='choices')
        nf1 = fs.non_form_errors()
        nf1.append('persisted')
        nf2 = fs.non_form_errors()
        self.assertIn('persisted', list(nf2))

    def test_appending_non_form_error_makes_formset_invalid(self):
        data = self._valid_choice_data()
        fs = ChoiceFormSet(data, auto_id=False, prefix='choices')
        nf = fs.non_form_errors()
        nf.append('fatal')
        self.assertFalse(fs.is_valid())

    def test_str_of_non_form_errors_includes_error_class_and_message(self):
        data = self._valid_choice_data()
        fs = ChoiceFormSet(data, auto_id=False, prefix='choices')
        nf = fs.non_form_errors()
        nf.append('Oops!')
        html = str(fs.non_form_errors())
        self.assertIn('Oops!', html)
        self.assertIn('errorlist nonform', html)

    def test_multiple_formsets_have_independent_non_form_errors(self):
        data1 = self._valid_choice_data(prefix='a')
        data2 = self._valid_choice_data(prefix='b')
        fs1 = ChoiceFormSet(data1, auto_id=False, prefix='a')
        fs2 = ChoiceFormSet(data2, auto_id=False, prefix='b')
        nf1 = fs1.non_form_errors()
        nf2 = fs2.non_form_errors()
        nf1.append('one-only')
        self.assertIn('one-only', list(fs1._non_form_errors))
        self.assertEqual(list(fs2._non_form_errors), [])

    def test_non_form_errors_html_reflects_mutation_between_calls(self):
        data = self._valid_choice_data()
        fs = ChoiceFormSet(data, auto_id=False, prefix='choices')
        nf = fs.non_form_errors()
        nf.append('HTML_ME')
        html1 = str(fs.non_form_errors())
        self.assertIn('HTML_ME', html1)
new_imports_code: ''