from django.test import RequestFactory
from django.test import RequestFactory
from .feeds import TestRss2Feed, TestRss2FeedWithGuidIsPermaLinkTrue, TestRss2FeedWithGuidIsPermaLinkFalse, TestRss091Feed, TestSingleEnclosureRSSFeed, TestMultipleEnclosureRSSFeed, TemplateFeed, TemplateContextFeed, TestLanguageFeed, TestFeedUrlFeed

def _render_feed(feed_cls):
    """
    Helper to render a feed class to a decoded string.
    """
    factory = RequestFactory()
    request = factory.get('/blog/')
    request.path = '/blog/'
    request.is_secure = lambda: False
    resp = feed_cls()(request)
    return resp.content.decode('utf-8')

def _assert_comments_before_category(feed_cls):
    content = _render_feed(feed_cls)
    item_pos = content.find('<item')
    assert item_pos != -1, 'No <item> found in feed output.'
    comments_pos = content.find('<comments>', item_pos)
    assert comments_pos != -1, 'No <comments> element found in feed output for %s.' % feed_cls.__name__
    category_pos = content.find('<category', item_pos)
    assert category_pos != -1, 'No <category> element found in feed output for %s.' % feed_cls.__name__
    assert comments_pos < category_pos, '<comments> should appear before <category> in the RSS item for %s.' % feed_cls.__name__

def test_rss2_comments_before_category():
    _assert_comments_before_category(TestRss2Feed)

def test_rss2_comments_before_category_guid_permalink_true():
    _assert_comments_before_category(TestRss2FeedWithGuidIsPermaLinkTrue)

def test_rss2_comments_before_category_guid_permalink_false():
    _assert_comments_before_category(TestRss2FeedWithGuidIsPermaLinkFalse)

def test_rss091_comments_before_category():
    _assert_comments_before_category(TestRss091Feed)

def test_single_enclosure_rss_comments_before_category():
    _assert_comments_before_category(TestSingleEnclosureRSSFeed)

def test_multiple_enclosure_rss_comments_before_category():
    _assert_comments_before_category(TestMultipleEnclosureRSSFeed)

def test_template_feed_comments_before_category():
    _assert_comments_before_category(TemplateFeed)

def test_template_context_feed_comments_before_category():
    _assert_comments_before_category(TemplateContextFeed)

def test_language_feed_comments_before_category():
    _assert_comments_before_category(TestLanguageFeed)

def test_feed_url_feed_comments_before_category():
    _assert_comments_before_category(TestFeedUrlFeed)

from types import SimpleNamespace
from django.test import TestCase
from django.http import HttpRequest
from django.utils.encoding import force_str
from types import SimpleNamespace
from django.test import TestCase
from django.http import HttpRequest
from django.utils.encoding import force_str
from .feeds import TestRss2Feed, TestRss091Feed, TestAtomFeed, TestLatestFeed, TestSingleEnclosureRSSFeed, TestSingleEnclosureAtomFeed, TemplateFeed, TemplateContextFeed, TestFeedUrlFeed, TestNoPubdateFeed
from .models import Entry

def make_request(domain='example.com', path='/blog/'):
    request = HttpRequest()
    request.site = SimpleNamespace(domain=domain)
    request.path = path
    request.is_secure = lambda: False
    return request

from django.test import TestCase, RequestFactory
from django.contrib.sites.models import Site
from django.http import HttpResponse
from django.utils import feedgenerator
from django.contrib.syndication import views
from types import SimpleNamespace

class CommentsPositionTests(TestCase):

    def setUp(self):
        self.site, _ = Site.objects.get_or_create(domain='example.com', defaults={'name': 'example.com'})
        self.factory = RequestFactory()

    def _make_item(self):

        class Item:

            def __init__(self, pk=1):
                self.pk = pk
                import datetime
                self.published = datetime.datetime(2001, 1, 1, 12, 0, 0)
                self.updated = datetime.datetime(2001, 1, 2, 12, 0, 0)

            def __str__(self):
                return 'Item%r' % (self.pk,)

            def get_absolute_url(self):
                return '/items/%d/' % (self.pk,)
        return Item()