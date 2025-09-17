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

from django.test import SimpleTestCase, RequestFactory
from django.http import HttpResponseNotAllowed, HttpResponse
from django.views.generic.base import View
import asyncio
try:
    from .tests import SyncView as _SyncView
    from .tests import AsyncView as _AsyncView
    SyncView = _SyncView
    AsyncView = _AsyncView
except Exception:

    class SyncView(View):

        def get(self, request, *args, **kwargs):
            return HttpResponse('Hello (sync) world!')

    class AsyncView(View):

        async def get(self, request, *args, **kwargs):
            return HttpResponse('Hello (async) world!')

class HttpMethodNotAllowedRegressionTests(SimpleTestCase):

    def setUp(self):
        self.rf = RequestFactory()
new_imports_code: ''