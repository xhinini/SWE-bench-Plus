from django.db import transaction, models
from django.db.models.deletion import Collector
from django.db import models
from django.db.models.deletion import Collector
from django.db import transaction
from django.test import TestCase
from .models import M, User, Avatar, Base, Child, R