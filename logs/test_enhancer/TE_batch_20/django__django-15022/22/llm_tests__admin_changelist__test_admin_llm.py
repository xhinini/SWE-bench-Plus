from django.test import TestCase, RequestFactory
from django.contrib import admin
from django.contrib.admin.options import ModelAdmin
from django.contrib.auth.models import User, AnonymousUser
from django.http import HttpRequest
from django.utils.encoding import force_str
from django.db import transaction
from django.db import connections
from django.test import TestCase, RequestFactory
from django.contrib import admin
from django.contrib.admin.options import ModelAdmin
from django.contrib.auth.models import User
from django.http import HttpRequest
from tests.admin_changelist.models import Child, Parent, Band, Event, Swallow
from tests.admin_changelist.admin import site as test_admin_site
rf = RequestFactory()