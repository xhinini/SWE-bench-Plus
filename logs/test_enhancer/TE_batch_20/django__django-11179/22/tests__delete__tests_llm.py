from django.test import TestCase
from django.db import models
from django.db.models.deletion import Collector
from .models import User, Avatar, M, R, HiddenUser, MR, M2MFrom, M2MTo, Parent, Child