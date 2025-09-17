from django.test import RequestFactory
from django.contrib import admin
from django.test import TestCase, RequestFactory
from django.contrib.admin import AdminSite, ModelAdmin
from django.contrib.auth.models import AnonymousUser
from django.db import transaction
from django.utils.http import urlencode
from tests.admin_changelist.models import Child, Parent