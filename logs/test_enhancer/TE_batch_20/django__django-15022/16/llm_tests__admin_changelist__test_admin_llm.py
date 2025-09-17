from django.test import RequestFactory
from django.contrib.auth.models import AnonymousUser
from django.test import TestCase, RequestFactory
from django.contrib.admin.options import ModelAdmin
from django.contrib.auth.models import AnonymousUser
from django.utils.safestring import mark_safe
from tests.admin_changelist.admin import site, ParentAdmin, ParentAdminTwoSearchFields, DynamicSearchFieldsChildAdmin
from tests.admin_changelist.models import Parent, Child