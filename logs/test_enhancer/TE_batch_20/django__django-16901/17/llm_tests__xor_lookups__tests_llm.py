from functools import reduce
from django.db.models import Q
from django.test import TestCase
from django.db import connection
import operator
from .models import Number