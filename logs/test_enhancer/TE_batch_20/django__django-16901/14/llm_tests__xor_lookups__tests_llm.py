from functools import reduce
import operator
from django.db.models import Q
from django.db import connection
from django.test import TestCase
from .models import Number