from unittest import mock
from django.contrib import admin
from django.contrib.admin.tests import AdminSeleniumTestCase
from django.db import DatabaseError
from django.test import TestCase, override_settings, skipUnlessDBFeature
from django.urls import reverse
from admin_changelist.models import Swallow