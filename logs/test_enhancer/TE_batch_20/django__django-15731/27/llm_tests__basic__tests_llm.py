from unittest import mock
import inspect
from django.test import SimpleTestCase
from django.db.models.manager import BaseManager
FakeQuerySet._private.queryset_only = None
FakeQuerySet.public_method.queryset_only = None
FakeQuerySet.method_with_varargs.queryset_only = None
FakeQuerySet.proxy_call.queryset_only = None
FakeQuerySet.all.queryset_only = None
QSWithExplicitUnderscore._exposed_private.queryset_only = False