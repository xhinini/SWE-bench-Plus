import datetime
from copy import copy
from django.db import connection
from django.db.models import CharField, Model
from django.test import isolate_apps