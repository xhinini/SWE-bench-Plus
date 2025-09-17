from django.core.validators import MaxLengthValidator
from copy import deepcopy
import pickle
from django.test import SimpleTestCase
from django import forms
from django.db.models import CharField
from django.core.validators import MaxLengthValidator