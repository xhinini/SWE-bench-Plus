from django.forms import Form, CharField, IntegerField
from django.forms.formsets import formset_factory
from django.forms.utils import ErrorList
from django.test import SimpleTestCase
ChoiceFormSet = formset_factory(Choice)
FavoriteDrinksFormSet = formset_factory(FavoriteDrinkForm, formset=BaseFavoriteDrinksFormSet, extra=2)