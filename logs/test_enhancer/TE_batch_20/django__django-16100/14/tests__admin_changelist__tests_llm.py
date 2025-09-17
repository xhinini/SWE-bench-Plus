from unittest import mock
from django.db import DatabaseError
from unittest import mock
from django.db import DatabaseError
from django.test import TestCase, override_settings
from django.urls import reverse
from django.contrib.auth.models import User
from .admin import SwallowAdmin
from .models import Swallow
from django.contrib import admin