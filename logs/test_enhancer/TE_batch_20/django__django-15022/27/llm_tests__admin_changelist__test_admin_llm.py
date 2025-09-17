from django.test.client import RequestFactory
from django.contrib.admin.sites import AdminSite
from django.test import TestCase
from django.test.client import RequestFactory
from django.contrib.auth.models import User
from django.contrib.admin.sites import AdminSite
from .admin import ParentAdmin, ParentAdminTwoSearchFields, ChildAdmin
from .models import Parent, Child