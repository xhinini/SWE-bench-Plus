from django.core.exceptions import ValidationError
from django.forms import Form, CharField, IntegerField
from django.forms.formsets import formset_factory, BaseFormSet
from django.forms.utils import ErrorList
from django.test import SimpleTestCase
ChoiceFormSet = formset_factory(SimpleChoice)
DuplicateDrinkFormSet = formset_factory(FavoriteDrink, formset=DuplicateCleanFormSet)