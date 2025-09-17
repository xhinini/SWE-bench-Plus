from copy import deepcopy
from django.db import connection
from django.db.models import CharField, Model
from django.test import TransactionTestCase, isolate_apps
from copy import deepcopy