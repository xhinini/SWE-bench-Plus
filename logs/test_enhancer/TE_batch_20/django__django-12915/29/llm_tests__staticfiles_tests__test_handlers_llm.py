from django.http import HttpRequest, HttpResponse, Http404
from django.test import SimpleTestCase, override_settings
import asyncio
from unittest.mock import patch
from unittest.mock import patch
import asyncio
from django.test import SimpleTestCase, override_settings
from django.http import HttpRequest, HttpResponse, Http404
from django.conf import settings
from urllib.parse import urlparse
from django.contrib.staticfiles.handlers import StaticFilesHandlerMixin, ASGIStaticFilesHandler
import django.contrib.staticfiles.handlers as handlers_module