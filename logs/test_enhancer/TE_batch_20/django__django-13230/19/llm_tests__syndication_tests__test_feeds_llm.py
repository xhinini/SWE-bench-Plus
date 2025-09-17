import io
from django.test import RequestFactory
from tests.syndication_tests import feeds as feed_defs
import io
from django.test import TestCase, RequestFactory
from tests.syndication_tests import feeds as feed_defs
from tests.syndication_tests.models import Entry
from django.contrib.syndication import views
from django.utils import feedgenerator