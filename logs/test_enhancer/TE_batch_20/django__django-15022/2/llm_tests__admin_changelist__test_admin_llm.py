from django.test import RequestFactory
from django.test import TestCase
from django.test import RequestFactory
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.admin.sites import AdminSite
from django.db import models
from tests.admin_changelist.models import Parent, Child, Band, Swallow
from tests.admin_changelist.admin import ParentAdmin, ParentAdminTwoSearchFields, DynamicSearchFieldsChildAdmin, BandAdmin, SwallowAdmin, site as test_site