from unittest import mock
import asyncio
from django.test import RequestFactory, SimpleTestCase
from django.http import HttpResponse, HttpResponseNotAllowed
from django.views.generic.base import View