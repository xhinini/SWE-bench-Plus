import copy
import pickle
from django.test import SimpleTestCase
from django.core import validators as core_validators
from django.core.exceptions import ValidationError
from django.db.models import CharField
from django.db.models.expressions import Value