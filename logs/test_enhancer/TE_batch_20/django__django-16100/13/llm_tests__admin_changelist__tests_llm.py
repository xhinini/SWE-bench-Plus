from unittest import mock
from django.contrib import admin
from django.contrib.auth.models import User
from django.db import DatabaseError, router
from django.test import TestCase, override_settings
from django.urls import reverse
from django.test.client import RequestFactory
from django.utils.http import urlencode
from admin_changelist.models import Swallow, Parent
from admin_changelist.admin import SwallowAdmin, ParentAdmin, site as custom_site