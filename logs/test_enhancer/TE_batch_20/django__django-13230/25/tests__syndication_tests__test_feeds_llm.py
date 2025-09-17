from django.test import RequestFactory, TestCase
import re
from django.test import RequestFactory, TestCase
from django.contrib.sites.models import Site
from django.contrib.syndication import views
from django.utils import feedgenerator
from django.utils.timezone import get_fixed_timezone
from django.template import loader, TemplateDoesNotExist
from tests.syndication_tests.models import Entry, Article
from tests.syndication_tests.feeds import TestRss2Feed, TestAtomFeed, TestRss091Feed
from django.core.exceptions import ImproperlyConfigured
import re
rf = RequestFactory()