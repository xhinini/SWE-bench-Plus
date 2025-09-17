import copy
import pickle
import copy
from django import forms
from django.core.exceptions import ValidationError
from django.db import models
from django.test import SimpleTestCase, TestCase
from django.utils.functional import lazy
from .models import Bar, Choiceful, Foo, RenamedField, VerboseNameField, Whiz, WhizDelayed, WhizIter, WhizIterEmpty