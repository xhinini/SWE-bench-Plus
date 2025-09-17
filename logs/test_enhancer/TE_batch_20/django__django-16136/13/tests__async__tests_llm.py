import asyncio
from unittest import mock
from django.core.exceptions import ImproperlyConfigured
from django.http import HttpResponse, HttpResponseNotAllowed, HttpResponseRedirect
from django.test import RequestFactory, SimpleTestCase
from django.views.generic.base import View, RedirectView