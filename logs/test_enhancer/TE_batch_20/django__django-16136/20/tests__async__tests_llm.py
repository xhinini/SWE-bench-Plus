from django.views.generic.base import View, RedirectView
import asyncio
from django.core.exceptions import ImproperlyConfigured
from django.http import HttpResponse, HttpResponseNotAllowed, HttpResponsePermanentRedirect, HttpResponseRedirect, HttpResponseGone
from django.test import RequestFactory, SimpleTestCase
from django.views.generic.base import View, RedirectView

def _maybe_await(value):
    if asyncio.iscoroutine(value):
        return asyncio.run(value)
    return value