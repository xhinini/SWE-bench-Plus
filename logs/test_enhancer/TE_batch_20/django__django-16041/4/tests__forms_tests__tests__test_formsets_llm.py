from django.forms.renderers import Jinja2
from django.test import SimpleTestCase
from django.forms.renderers import Jinja2
from django.forms.formsets import formset_factory
from .test_formsets import Choice, CustomKwargForm

class EmptyFormKwargsRegressionTests(SimpleTestCase):

    def test_prefix_not_overridden_by_form_kwargs(self):
        ChoiceFormSet = formset_factory(Choice)
        formset = ChoiceFormSet(prefix='myform', form_kwargs={'prefix': 'evil'}, auto_id=False)
        self.assertEqual(formset.empty_form.prefix, formset.add_prefix('__prefix__'))
        self.assertEqual(formset.empty_form.prefix, 'myform-__prefix__')

    def test_auto_id_not_overridden_by_form_kwargs(self):
        ChoiceFormSet = formset_factory(Choice)
        formset = ChoiceFormSet(auto_id='id_custom_%s', form_kwargs={'auto_id': 'evil'}, prefix='pfx')
        self.assertEqual(formset.empty_form.auto_id, formset.auto_id)
        self.assertEqual(formset.empty_form.auto_id, 'id_custom_%s')

    def test_renderer_not_overridden_by_form_kwargs(self):
        r1 = Jinja2()
        r2 = Jinja2()
        ChoiceFormSet = formset_factory(Choice, renderer=r1)
        formset = ChoiceFormSet(form_kwargs={'renderer': r2})
        self.assertIs(formset.empty_form.renderer, r1)

    def test_renderer_none_in_form_kwargs_is_ignored(self):
        r1 = Jinja2()
        ChoiceFormSet = formset_factory(Choice, renderer=r1)
        formset = ChoiceFormSet(form_kwargs={'renderer': None})
        self.assertIs(formset.empty_form.renderer, r1)

    def test_use_required_attribute_not_overridden_by_form_kwargs(self):
        ChoiceFormSet = formset_factory(Choice)
        formset = ChoiceFormSet(form_kwargs={'use_required_attribute': True}, prefix='choices')
        self.assertIs(formset.empty_form.use_required_attribute, False)

    def test_prefix_none_in_form_kwargs_does_not_override(self):
        ChoiceFormSet = formset_factory(Choice)
        formset = ChoiceFormSet(prefix='x', form_kwargs={'prefix': None})
        self.assertEqual(formset.empty_form.prefix, formset.add_prefix('__prefix__'))

    def test_auto_id_false_in_form_kwargs_does_not_override(self):
        ChoiceFormSet = formset_factory(Choice)
        formset = ChoiceFormSet(auto_id='id_want_%s', form_kwargs={'auto_id': False})
        self.assertEqual(formset.empty_form.auto_id, 'id_want_%s')

    def test_use_required_attribute_false_overrides_form_kwargs_true(self):
        ChoiceFormSet = formset_factory(Choice)
        formset = ChoiceFormSet(form_kwargs={'use_required_attribute': True})
        self.assertIs(formset.empty_form.use_required_attribute, False)

from django.test import SimpleTestCase
from django.forms.formsets import formset_factory
from django.forms import Form
from .test_formsets import CustomKwargForm

class EmptyFormKwargsRegressionTests(SimpleTestCase):

    def test_empty_form_with_form_kwargs_auto_id_does_not_raise_and_uses_formset_auto_id(self):
        FormSet = formset_factory(CustomKwargForm)
        fs = FormSet(form_kwargs={'custom_kwarg': 1, 'auto_id': 'bad_auto'}, prefix='pfx', auto_id='id_%s')
        empty = fs.empty_form
        self.assertEqual(empty.custom_kwarg, 1)
        self.assertEqual(empty.auto_id, fs.auto_id)

    def test_empty_form_with_form_kwargs_prefix_does_not_override(self):
        FormSet = formset_factory(CustomKwargForm)
        fs = FormSet(form_kwargs={'custom_kwarg': 2, 'prefix': 'bad_prefix'}, prefix='pfx')
        empty = fs.empty_form
        self.assertEqual(empty.custom_kwarg, 2)
        self.assertEqual(empty.prefix, fs.add_prefix('__prefix__'))

    def test_empty_form_use_required_attribute_false_even_if_overridden_in_form_kwargs(self):
        FormSet = formset_factory(CustomKwargForm)
        fs = FormSet(form_kwargs={'custom_kwarg': 4, 'use_required_attribute': True})
        empty = fs.empty_form
        self.assertEqual(empty.custom_kwarg, 4)
        self.assertFalse(empty.use_required_attribute)

    def test_empty_form_renderer_precedence_ignores_renderer_in_form_kwargs(self):
        sentinel_renderer = object()
        other_renderer = object()
        FormSet = formset_factory(CustomKwargForm, renderer=sentinel_renderer)
        fs = FormSet(form_kwargs={'custom_kwarg': 5, 'renderer': other_renderer})
        empty = fs.empty_form
        self.assertIs(empty.renderer, sentinel_renderer)

    def test_empty_form_with_both_auto_id_and_prefix_in_form_kwargs_does_not_raise(self):
        FormSet = formset_factory(CustomKwargForm)
        fs = FormSet(form_kwargs={'custom_kwarg': 6, 'auto_id': 'bad_auto', 'prefix': 'bad_prefix'}, prefix='realprefix')
        empty = fs.empty_form
        self.assertEqual(empty.custom_kwarg, 6)
        self.assertEqual(empty.auto_id, fs.auto_id)
        self.assertEqual(empty.prefix, fs.add_prefix('__prefix__'))

    def test_empty_form_with_auto_id_prefix_and_renderer_in_form_kwargs(self):
        sentinel_renderer = object()
        other_renderer = object()
        FormSet = formset_factory(CustomKwargForm, renderer=sentinel_renderer)
        fs = FormSet(form_kwargs={'custom_kwarg': 7, 'auto_id': 'bad_auto', 'prefix': 'bad_prefix', 'renderer': other_renderer}, prefix='realprefix')
        empty = fs.empty_form
        self.assertEqual(empty.custom_kwarg, 7)
        self.assertEqual(empty.auto_id, fs.auto_id)
        self.assertEqual(empty.prefix, fs.add_prefix('__prefix__'))
        self.assertIs(empty.renderer, sentinel_renderer)

    def test_no_type_error_with_all_overlapping_keys_present(self):
        sentinel_renderer = object()
        other_renderer = object()
        FormSet = formset_factory(CustomKwargForm, renderer=sentinel_renderer)
        fs = FormSet(prefix='pp', form_kwargs={'custom_kwarg': 8, 'auto_id': 'bad', 'prefix': 'bad', 'renderer': other_renderer, 'empty_permitted': False, 'use_required_attribute': True})
        empty = fs.empty_form
        self.assertEqual(empty.custom_kwarg, 8)
        self.assertEqual(empty.auto_id, fs.auto_id)
        self.assertEqual(empty.prefix, fs.add_prefix('__prefix__'))
        self.assertIs(empty.renderer, sentinel_renderer)
        self.assertTrue(empty.empty_permitted)
        self.assertFalse(empty.use_required_attribute)