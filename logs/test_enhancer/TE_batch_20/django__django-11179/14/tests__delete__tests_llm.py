from django.db import transaction
from django.test import TestCase
from .models import User, Avatar
from django.db.models.deletion import Collector