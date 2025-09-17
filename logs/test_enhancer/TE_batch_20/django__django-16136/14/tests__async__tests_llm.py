import asyncio
from django.test import RequestFactory, SimpleTestCase
from django.http import HttpResponse, HttpResponseNotAllowed, HttpResponseGone
from django.core.exceptions import ImproperlyConfigured
from django.views.generic.base import View, RedirectView, TemplateResponseMixin
import asyncio
from django.test import SimpleTestCase, RequestFactory
from django.http import HttpResponse, HttpResponseNotAllowed, HttpResponseGone, HttpResponseRedirect, HttpResponsePermanentRedirect
from django.core.exceptions import ImproperlyConfigured
from django.views.generic.base import View, RedirectView, TemplateResponseMixin