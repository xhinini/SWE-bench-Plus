from django.db import connection, models, transaction
from django.db.models.deletion import Collector
from django.db import connection, models
from django.test import TestCase, skipUnlessDBFeature, override_settings
from django.db.models.deletion import Collector
from django.db import transaction
from .models import User, Avatar, M2MFrom, M2MTo