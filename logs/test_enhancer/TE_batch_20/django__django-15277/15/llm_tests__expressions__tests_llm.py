from copy import deepcopy
from django import forms
from django.core import validators, exceptions
from django.test import SimpleTestCase
from django.db.models import CharField, SlugField