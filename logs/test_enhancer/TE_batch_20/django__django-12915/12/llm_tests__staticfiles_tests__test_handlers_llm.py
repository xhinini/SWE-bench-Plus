from urllib.parse import urlparse
import asyncio
from django.test import SimpleTestCase, override_settings
from django.http import Http404
import django.contrib.staticfiles.handlers as handlers
from django.contrib.staticfiles.handlers import StaticFilesHandlerMixin, ASGIStaticFilesHandler