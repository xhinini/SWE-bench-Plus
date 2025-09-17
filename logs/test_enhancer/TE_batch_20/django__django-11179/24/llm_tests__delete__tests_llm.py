from django.db.models.deletion import Collector
from django.db.models import signals
from django.db import transaction
from django.db import models
from django.db.models.deletion import Collector
from django.db import transaction
from django.test import TestCase
from django.db import models as dj_models
from django.db.models import signals
from .models import User, Avatar, Child, Parent, RChild