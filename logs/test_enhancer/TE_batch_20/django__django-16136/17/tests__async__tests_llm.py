import asyncio
from django.http import HttpResponse, HttpResponseNotAllowed
from django.test import RequestFactory, SimpleTestCase
from django.views.generic.base import View