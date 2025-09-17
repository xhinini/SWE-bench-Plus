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

from types import SimpleNamespace
from unittest.mock import patch
from django.test import RequestFactory
from django.http import HttpResponse
from types import SimpleNamespace
from unittest.mock import patch
from django.contrib.syndication import views
from django.utils import feedgenerator
from django.test import RequestFactory
from django.http import HttpResponse

def render_feed(feed_instance, request):
    feedgen = feed_instance.get_feed(None, request)
    response = HttpResponse(content_type=feedgen.content_type)
    feedgen.write(response, 'utf-8')
    return response.content.decode('utf-8')

def make_request(path='/feed/', secure=False):
    rf = RequestFactory()
    req = rf.get(path)
    if secure:
        req._is_secure_override = True
        req.is_secure = lambda: True
    else:
        req._is_secure_override = False
        req.is_secure = lambda: False
    return req

def test_comments_before_category_callable_with_item():

    class MyFeed(views.Feed):
        title = 'T'
        link = '/'
        feed_type = feedgenerator.Rss201rev2Feed

        def items(self):

            class I:

                def get_absolute_url(self):
                    return '/item/1/'

                def __str__(self):
                    return 'item1'
            return [I()]

        def item_comments(self, item):
            return 'http://example.com/comments/1'

        def item_categories(self, item):
            return ['news']

        def item_copyright(self, item):
            return 'Copyright 2020'
    feed = MyFeed()
    req = make_request()
    with patch('django.contrib.syndication.views.get_current_site', return_value=SimpleNamespace(domain='example.com')):
        xml = render_feed(feed, req)
    assert '<comments>' in xml
    assert xml.index('<comments>') < xml.index('<category>')
    assert xml.index('<comments>') < xml.index('<copyright>')

def test_comments_before_category_callable_no_args():

    class MyFeed(views.Feed):
        title = 'T'
        link = '/'
        feed_type = feedgenerator.Rss201rev2Feed

        def items(self):

            class I:

                def get_absolute_url(self):
                    return '/item/2/'

                def __str__(self):
                    return 'item2'
            return [I()]

        def item_comments(self):
            return 'http://example.com/comments/2'

        def item_categories(self, item):
            return ['misc']

        def item_copyright(self, item):
            return 'Copyright 2021'
    feed = MyFeed()
    req = make_request()
    with patch('django.contrib.syndication.views.get_current_site', return_value=SimpleNamespace(domain='example.com')):
        xml = render_feed(feed, req)
    assert '<comments>' in xml
    assert xml.index('<comments>') < xml.index('<category>')
    assert xml.index('<comments>') < xml.index('<copyright>')

def test_comments_before_category_attribute_string():

    class MyFeed(views.Feed):
        title = 'T'
        link = '/'
        feed_type = feedgenerator.Rss201rev2Feed
        item_comments = 'http://example.com/comments/static'

        def items(self):

            class I:

                def get_absolute_url(self):
                    return '/item/3/'

                def __str__(self):
                    return 'item3'
            return [I()]

        def item_categories(self, item):
            return ['cat']

        def item_copyright(self, item):
            return 'Copyright 2022'
    feed = MyFeed()
    req = make_request()
    with patch('django.contrib.syndication.views.get_current_site', return_value=SimpleNamespace(domain='example.com')):
        xml = render_feed(feed, req)
    assert '<comments>' in xml
    assert xml.index('<comments>') < xml.index('<category>')
    assert xml.index('<comments>') < xml.index('<copyright>')

def test_comments_once_per_item_and_ordering_multiple_items():

    class MyFeed(views.Feed):
        title = 'T'
        link = '/'
        feed_type = feedgenerator.Rss201rev2Feed

        def items(self):

            class I:

                def __init__(self, n):
                    self.n = n

                def get_absolute_url(self):
                    return f'/item/{self.n}/'

                def __str__(self):
                    return f'item{self.n}'
            return [I(1), I(2)]

        def item_comments(self, item):
            return f'http://example.com/comments/{item.n}'

        def item_categories(self, item):
            return ['a']

        def item_copyright(self, item):
            return f'Copyright {item.n}'
    feed = MyFeed()
    req = make_request()
    with patch('django.contrib.syndication.views.get_current_site', return_value=SimpleNamespace(domain='example.com')):
        xml = render_feed(feed, req)
    assert xml.count('<comments>') == 2
    first_comments = xml.index('<comments>')
    first_category = xml.index('<category>')
    first_copyright = xml.index('<copyright>')
    assert first_comments < first_category
    assert first_comments < first_copyright

def test_comments_before_category_rss091():

    class MyFeed(views.Feed):
        title = 'T'
        link = '/'
        feed_type = feedgenerator.RssUserland091Feed

        def items(self):

            class I:

                def get_absolute_url(self):
                    return '/item/091/'

                def __str__(self):
                    return 'item091'
            return [I()]

        def item_comments(self, item):
            return 'http://example.com/comments/091'

        def item_categories(self, item):
            return ['old']

        def item_copyright(self, item):
            return 'Copyright091'
    feed = MyFeed()
    req = make_request()
    with patch('django.contrib.syndication.views.get_current_site', return_value=SimpleNamespace(domain='example.com')):
        xml = render_feed(feed, req)
    assert '<comments>' in xml
    assert xml.index('<comments>') < xml.index('<category>')
    assert xml.index('<comments>') < xml.index('<copyright>')

def test_comments_before_category_with_guid_is_permalink_true():

    class BaseFeed(views.Feed):
        title = 'T'
        link = '/'
        feed_type = feedgenerator.Rss201rev2Feed

        def items(self):

            class I:

                def get_absolute_url(self):
                    return '/item/g1/'

                def __str__(self):
                    return 'itemg1'
            return [I()]

        def item_comments(self, item):
            return 'http://example.com/comments/g1'

        def item_categories(self, item):
            return ['x']

        def item_copyright(self, item):
            return 'C-G1'

    class SubFeed(BaseFeed):

        def item_guid_is_permalink(self, item):
            return True
    feed = SubFeed()
    req = make_request()
    with patch('django.contrib.syndication.views.get_current_site', return_value=SimpleNamespace(domain='example.com')):
        xml = render_feed(feed, req)
    assert '<comments>' in xml
    assert xml.index('<comments>') < xml.index('<category>')
    assert xml.index('<comments>') < xml.index('<copyright>')

def test_comments_before_category_with_guid_is_permalink_false():

    class BaseFeed(views.Feed):
        title = 'T'
        link = '/'
        feed_type = feedgenerator.Rss201rev2Feed

        def items(self):

            class I:
                pk = 99

                def get_absolute_url(self):
                    return '/item/g2/'

                def __str__(self):
                    return 'itemg2'
            return [I()]

        def item_guid(self, item):
            return 'custom-guid'

        def item_guid_is_permalink(self, item):
            return False

        def item_comments(self, item):
            return 'http://example.com/comments/g2'

        def item_categories(self, item):
            return ['y']

        def item_copyright(self, item):
            return 'C-G2'
    feed = BaseFeed()
    req = make_request()
    with patch('django.contrib.syndication.views.get_current_site', return_value=SimpleNamespace(domain='example.com')):
        xml = render_feed(feed, req)
    assert '<comments>' in xml
    assert xml.index('<comments>') < xml.index('<category>')
    assert xml.index('<comments>') < xml.index('<copyright>')

def test_no_comments_tag_when_none():

    class MyFeed(views.Feed):
        title = 'T'
        link = '/'
        feed_type = feedgenerator.Rss201rev2Feed

        def items(self):

            class I:

                def get_absolute_url(self):
                    return '/item/nc/'

                def __str__(self):
                    return 'itemnc'
            return [I()]

        def item_comments(self, item):
            return None

        def item_categories(self, item):
            return ['noc']

        def item_copyright(self, item):
            return 'NoComments'
    feed = MyFeed()
    req = make_request()
    with patch('django.contrib.syndication.views.get_current_site', return_value=SimpleNamespace(domain='example.com')):
        xml = render_feed(feed, req)
    assert '<comments>' not in xml

def test_comments_before_category_callable_object():

    class CallableObj:

        def __call__(self, item):
            return 'http://example.com/comments/callableobj'

    class MyFeed(views.Feed):
        title = 'T'
        link = '/'
        feed_type = feedgenerator.Rss201rev2Feed
        item_comments = CallableObj()

        def items(self):

            class I:

                def get_absolute_url(self):
                    return '/item/co/'

                def __str__(self):
                    return 'itemco'
            return [I()]

        def item_categories(self, item):
            return ['z']

        def item_copyright(self, item):
            return 'C-CO'
    feed = MyFeed()
    req = make_request()
    with patch('django.contrib.syndication.views.get_current_site', return_value=SimpleNamespace(domain='example.com')):
        xml = render_feed(feed, req)
    assert '<comments>' in xml
    assert xml.index('<comments>') < xml.index('<category>')
    assert xml.index('<comments>') < xml.index('<copyright>')

def test_comments_content_appears():
    url = 'http://example.com/specific-comments-url'

    class MyFeed(views.Feed):
        title = 'T'
        link = '/'
        feed_type = feedgenerator.Rss201rev2Feed

        def items(self):

            class I:

                def get_absolute_url(self):
                    return '/item/content/'

                def __str__(self):
                    return 'itemcontent'
            return [I()]

        def item_comments(self, item):
            return url

        def item_categories(self, item):
            return ['c']

        def item_copyright(self, item):
            return 'C-CONT'
    feed = MyFeed()
    req = make_request()
    with patch('django.contrib.syndication.views.get_current_site', return_value=SimpleNamespace(domain='example.com')):
        xml = render_feed(feed, req)
    assert '<comments>' in xml
    assert url in xml

import io
from types import SimpleNamespace
from unittest.mock import patch
from django.utils import feedgenerator
from django.contrib.syndication import views
import io
import unittest
from types import SimpleNamespace
from unittest.mock import patch
from django.utils import feedgenerator
from django.contrib.syndication import views

def render_feed(feed_instance):
    with patch('django.contrib.syndication.views.get_current_site') as mocked_site:
        mocked_site.return_value = SimpleNamespace(domain='example.com')
        request = SimpleNamespace(path='/feed/', is_secure=lambda: False)
        feedobj = feed_instance.get_feed(None, request)
        buf = io.BytesIO()
        feedobj.write(buf, 'utf-8')
        return buf.getvalue().decode('utf-8')
if __name__ == '__main__':
    unittest.main()

import io
import unittest
from types import SimpleNamespace
from unittest.mock import patch
from django.contrib.syndication import views
from django.utils import feedgenerator
import io
import unittest
from types import SimpleNamespace
from unittest.mock import patch
from django.contrib.syndication import views
from django.utils import feedgenerator

def render_feed_to_string(feedobj, request):
    """
    Helper to get the feed output as a string.
    """
    feed = feedobj.get_feed(None, request)
    buf = io.BytesIO()
    feed.write(buf, 'utf-8')
    return buf.getvalue().decode('utf-8')
if __name__ == '__main__':
    unittest.main()

import io
import unittest
from types import SimpleNamespace
from django.utils import feedgenerator
from django.contrib.syndication import views

def _stub_site(domain='example.com'):
    return SimpleNamespace(domain=domain)
if __name__ == '__main__':
    unittest.main()