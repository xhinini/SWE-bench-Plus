from django.contrib import admin
from django.contrib.admin.sites import AdminSite
from django.test import TestCase
from django.contrib import admin
from django.contrib.admin.sites import AdminSite
from tests.admin_changelist.models import Parent, Child
site = AdminSite(name='test')