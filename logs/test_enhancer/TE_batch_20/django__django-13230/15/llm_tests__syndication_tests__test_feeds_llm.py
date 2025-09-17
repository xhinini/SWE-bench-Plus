from django.test import RequestFactory, TestCase
from django.contrib.sites.models import Site
from django.utils import timezone
from django.conf import settings
from django.test import RequestFactory, TestCase
from django.contrib.sites.models import Site
from django.utils import timezone
from django.utils.feedgenerator import Atom1Feed
from django.conf import settings
from tests.syndication_tests.feeds import TestRss2Feed, TestRss091Feed, TestAtomFeed, TemplateFeed, TestSingleEnclosureRSSFeed, TestMultipleEnclosureAtomFeed, TestFeedUrlFeed
from tests.syndication_tests.models import Entry, Article