from django.test import TestCase
from django.db import models
from django.db.models.deletion import Collector
from .models import User, Avatar, Base, M, M2MTo, MR, Child, Parent, R, RChild, create_a, get_default_r