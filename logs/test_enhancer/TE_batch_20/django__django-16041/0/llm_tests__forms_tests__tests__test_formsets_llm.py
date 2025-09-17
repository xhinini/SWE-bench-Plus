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