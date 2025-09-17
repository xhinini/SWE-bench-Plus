from django.test import TestCase
from django.contrib import admin
from django.contrib.admin.options import ModelAdmin
from tests.admin_changelist.models import Parent, Child
from tests.admin_changelist.admin import site, ParentAdminTwoSearchFields