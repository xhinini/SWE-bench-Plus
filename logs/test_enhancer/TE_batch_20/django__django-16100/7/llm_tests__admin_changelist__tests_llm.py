from django.test import TestCase
from unittest import mock
from django.db import DatabaseError
from django.urls import reverse
from django.contrib.admin import options as admin_options
from unittest import mock
from django.db import DatabaseError
from django.urls import reverse
from django.contrib.admin import options as admin_options
from django.contrib.admin.tests import AdminSeleniumTestCase
from .models import Swallow
from .admin import SwallowAdmin
from django.contrib.auth.models import User