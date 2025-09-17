from io import StringIO
from types import SimpleNamespace
from unittest.mock import patch
from datetime import datetime
from django.test import TestCase, RequestFactory
from django.utils import feedgenerator
from django.utils.timezone import get_default_timezone, make_aware
from django.contrib.syndication import views