from django.test import RequestFactory
from django.test import TestCase, RequestFactory
from django.contrib import admin
from django.db import models
from tests.admin_changelist.admin import ParentAdmin, ParentAdminTwoSearchFields, ChildAdmin, DynamicSearchFieldsChildAdmin, DynamicListDisplayChildAdmin, site as test_site
from tests.admin_changelist.models import Parent, Child