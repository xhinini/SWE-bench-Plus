from typing import NamedTuple as TypingNamedTuple
from collections import namedtuple
from typing import NamedTuple as TypingNamedTuple
from django.test import TestCase
from django.db.models import F, Value
from django.db.models.fields import IntegerField
from .models import Company, Employee, Number, Experiment, Time, SimulationRun, Result
import datetime