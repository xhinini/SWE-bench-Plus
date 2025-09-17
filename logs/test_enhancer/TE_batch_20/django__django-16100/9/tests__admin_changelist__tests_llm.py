from unittest import mock
from django.test import TestCase, RequestFactory, override_settings
from django.urls import reverse
from django.contrib.messages.storage.cookie import CookieStorage
from django.db import DatabaseError
from django.db import router
from admin_changelist.admin import SwallowAdmin
from admin_changelist.models import Swallow
from admin_changelist import admin as custom_site