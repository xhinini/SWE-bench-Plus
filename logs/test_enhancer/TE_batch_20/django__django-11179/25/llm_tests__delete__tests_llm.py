from django.test import TestCase
from django.db import models
from django.db import connection
from django.db.models.deletion import Collector
from .models import User, Avatar, Child, Parent, RChild, HiddenUser, HiddenUserProfile, M