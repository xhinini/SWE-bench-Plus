import asyncio
from django.test import SimpleTestCase, RequestFactory
from django.http import HttpResponse, HttpResponseNotAllowed, HttpResponseGone
from django.views.generic.base import View, RedirectView