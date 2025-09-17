from functools import reduce
import operator
from django.db.models import Q
from django.test import TestCase
from django.db import connection
from .models import Number