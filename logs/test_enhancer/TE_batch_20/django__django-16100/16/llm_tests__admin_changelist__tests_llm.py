from unittest.mock import patch, MagicMock
from unittest.mock import patch, MagicMock
from django.test import TestCase
from django.test.client import RequestFactory
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.db import DatabaseError
from django.contrib import admin
from django.contrib.admin.options import ModelAdmin
from django.contrib.admin.tests import AdminSeleniumTestCase
from django.contrib.admin.views.main import ALL_VAR
from django.db import router
from .models import Swallow