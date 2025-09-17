from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User
from django.contrib import admin
from django.db import connection
from tests.admin_changelist.admin import site as test_admin_site, ParentAdmin, ParentAdminTwoSearchFields, ChildAdmin, ConcertAdmin, DynamicSearchFieldsChildAdmin
from tests.admin_changelist.models import Parent, Child, Group, Band