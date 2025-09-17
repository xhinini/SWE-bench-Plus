from unittest.mock import patch
from django.db import connection
from functools import reduce
import operator
from unittest.mock import patch
from django.db import connection
from django.db.models import Q
from django.test import TestCase
from .models import Number