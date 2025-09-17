from unittest import mock
from django.contrib import admin
from django.contrib.admin.options import router as options_router
from django.contrib.admin.options import transaction as options_transaction
from django.core.exceptions import ValidationError
from django.db import DatabaseError, router
from django.test import TransactionTestCase, override_settings
from django.urls import reverse
from admin_changelist.models import Swallow
from admin_changelist.admin import SwallowAdmin