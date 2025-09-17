from django import forms
from django.core import validators as core_validators
from django.test import SimpleTestCase
from django.db.models import CharField
from django.utils.module_loading import import_string
MaxLengthValidator = core_validators.MaxLengthValidator