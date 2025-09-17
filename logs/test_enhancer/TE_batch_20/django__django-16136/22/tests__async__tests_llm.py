from django.test import RequestFactory, SimpleTestCase
from django.http import HttpResponseNotAllowed, HttpResponse
import asyncio
from django.views.generic.base import View, RedirectView