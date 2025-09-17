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

import io
from types import SimpleNamespace
import pytest
from django.contrib.syndication import views
from django.utils import feedgenerator
import io
from types import SimpleNamespace
import pytest
from django.contrib.syndication import views
from django.utils import feedgenerator
views.get_current_site = lambda request: SimpleNamespace(domain='example.com')

def render_feed_xml(feed_instance):
    """
    Helper that produces the feed XML as a string for assertions.
    """
    request = SimpleNamespace(path='/feed/', is_secure=lambda: False)
    feedgen = feed_instance.get_feed(None, request)
    buf = io.BytesIO()
    feedgen.write(buf, 'utf-8')
    return buf.getvalue().decode('utf-8')

def make_feed_class(feed_type=feedgenerator.DefaultFeed, item_categories=None, item_copyright=None, author_name='Author', item_comments_value='/items/1/#c'):
    """
    Factory to create a Feed subclass configured for the tests.
    """
    item_categories = item_categories

    class CustomFeed(views.Feed):
        title = 'Test'
        link = '/test/'
        feed_type = feed_type
        author_name = author_name

        def items(self):
            return [DummyItem(1)]

        def item_link(self, item):
            return item.get_absolute_url()

        def item_comments(self, item):
            return item_comments_value
        if item_categories is not None:
            item_categories = item_categories
        if item_copyright is not None:
            item_copyright = item_copyright
    return CustomFeed()

def test_comments_before_category_in_rss2():
    feed = make_feed_class(feed_type=feedgenerator.Rss201rev2Feed, item_categories=('news',))
    xml = render_feed_xml(feed)
    assert '<comments>' in xml
    assert '<category>' in xml
    assert xml.index('<comments>') < xml.index('<category>')

def test_comments_before_category_with_multiple_categories_rss2():
    feed = make_feed_class(feed_type=feedgenerator.Rss201rev2Feed, item_categories=('news', 'django', 'python'))
    xml = render_feed_xml(feed)
    assert '<comments>' in xml
    assert xml.index('<comments>') < xml.index('<category>')

def test_comments_before_copyright_in_rss2():
    feed = make_feed_class(feed_type=feedgenerator.Rss201rev2Feed, item_categories=('news',), item_copyright='Copyright (c) ACME')
    xml = render_feed_xml(feed)
    assert '<comments>' in xml
    assert '<copyright>' in xml
    assert xml.index('<comments>') < xml.index('<copyright>')

def test_comments_before_category_when_no_author_rss2():
    feed = make_feed_class(feed_type=feedgenerator.Rss201rev2Feed, item_categories=('news',), author_name=None)
    xml = render_feed_xml(feed)
    assert '<comments>' in xml
    assert '<category>' in xml
    assert xml.index('<comments>') < xml.index('<category>')

def test_no_comments_tag_when_item_comments_returns_none_rss2():
    feed = make_feed_class(feed_type=feedgenerator.Rss201rev2Feed, item_categories=('news',), item_comments_value=None)
    xml = render_feed_xml(feed)
    assert '<comments>' not in xml

def test_comments_before_category_in_rss091():
    feed = make_feed_class(feed_type=feedgenerator.RssUserland091Feed, item_categories=('news',))
    xml = render_feed_xml(feed)
    assert '<comments>' in xml
    assert '<category>' in xml
    assert xml.index('<comments>') < xml.index('<category>')

def test_comments_before_category_with_multiple_categories_rss091():
    feed = make_feed_class(feed_type=feedgenerator.RssUserland091Feed, item_categories=('a', 'b', 'c'))
    xml = render_feed_xml(feed)
    assert '<comments>' in xml
    assert xml.index('<comments>') < xml.index('<category>')

def test_comments_before_copyright_in_rss091():
    feed = make_feed_class(feed_type=feedgenerator.RssUserland091Feed, item_categories=('news',), item_copyright='© 2025')
    xml = render_feed_xml(feed)
    assert '<comments>' in xml
    assert '<copyright>' in xml
    assert xml.index('<comments>') < xml.index('<copyright>')

def test_comments_before_category_when_no_author_rss091():
    feed = make_feed_class(feed_type=feedgenerator.RssUserland091Feed, item_categories=('news',), author_name=None)
    xml = render_feed_xml(feed)
    assert '<comments>' in xml
    assert '<category>' in xml
    assert xml.index('<comments>') < xml.index('<category>')

from django.test import RequestFactory
import xml.etree.ElementTree as ET
from django.test import RequestFactory
from django.utils import feedgenerator
import xml.etree.ElementTree as ET
from .feeds import TestRss2Feed, TestRss2FeedWithGuidIsPermaLinkTrue, TestRss2FeedWithGuidIsPermaLinkFalse, TestRss091Feed, ArticlesFeed, TestSingleEnclosureRSSFeed, TestMultipleEnclosureRSSFeed, TemplateFeed, TemplateContextFeed, TestLanguageFeed
rf = RequestFactory()

def _get_first_item_children(feed_class):
    """
    Helper that instantiates the feed class, requests the feed, parses the
    resulting XML, and returns the list of child tag local-names for the
    first <item> element.
    """
    request = rf.get('/', HTTP_HOST='example.com')
    feed = feed_class()
    response = feed(request)
    content = response.content
    root = ET.fromstring(content)
    item = None
    for elem in root.iter():
        tag = elem.tag
        if '}' in tag:
            local = tag.split('}', 1)[1]
        else:
            local = tag
        if local == 'item':
            item = elem
            break
    assert item is not None, 'No <item> found in feed output for %s' % feed_class.__name__
    children_local_names = []
    for child in list(item):
        tag = child.tag
        if '}' in tag:
            local = tag.split('}', 1)[1]
        else:
            local = tag
        children_local_names.append(local)
    return children_local_names

def _assert_comments_before_category_and_copyright(feed_class):
    children = _get_first_item_children(feed_class)
    assert 'comments' in children, '%s: <comments> not present' % feed_class.__name__
    assert 'category' in children, '%s: <category> not present' % feed_class.__name__
    assert 'copyright' in children or 'item_copyright' in children or 'rights' in children, '%s: copyright-like tag not present' % feed_class.__name__
    comments_index = children.index('comments')
    category_index = children.index('category')
    if 'copyright' in children:
        copyright_index = children.index('copyright')
    elif 'item_copyright' in children:
        copyright_index = children.index('item_copyright')
    else:
        copyright_index = children.index('rights')
    assert comments_index < category_index, '%s: <comments> should come before <category>' % feed_class.__name__
    assert comments_index < copyright_index, '%s: <comments> should come before copyright element' % feed_class.__name__

def test_rss2_comments_position():
    _assert_comments_before_category_and_copyright(TestRss2Feed)

def test_rss2_with_guid_permalink_true_comments_position():
    _assert_comments_before_category_and_copyright(TestRss2FeedWithGuidIsPermaLinkTrue)

def test_rss2_with_guid_permalink_false_comments_position():
    _assert_comments_before_category_and_copyright(TestRss2FeedWithGuidIsPermaLinkFalse)

def test_rss091_comments_position():
    _assert_comments_before_category_and_copyright(TestRss091Feed)

def test_articles_feed_comments_position():
    _assert_comments_before_category_and_copyright(ArticlesFeed)

def test_single_enclosure_rss_feed_comments_position():
    _assert_comments_before_category_and_copyright(TestSingleEnclosureRSSFeed)

def test_multiple_enclosure_rss_feed_comments_position():
    _assert_comments_before_category_and_copyright(TestMultipleEnclosureRSSFeed)

def test_template_feed_comments_position():
    _assert_comments_before_category_and_copyright(TemplateFeed)

def test_template_context_feed_comments_position():
    _assert_comments_before_category_and_copyright(TemplateContextFeed)

def test_language_feed_comments_position():
    _assert_comments_before_category_and_copyright(TestLanguageFeed)

from unittest.mock import patch
from django.test import RequestFactory
from django.http import HttpResponse
from types import SimpleNamespace
from types import SimpleNamespace
from unittest.mock import patch
from django.http import HttpResponse
from django.test import RequestFactory
from django.utils import feedgenerator
from django.contrib.syndication import views
import datetime

def _render_feed(feed_instance, path='/feed/'):
    rf = RequestFactory()
    request = rf.get(path)
    with patch('django.contrib.syndication.views.get_current_site', return_value=SimpleNamespace(domain='example.com')):
        fg = feed_instance.get_feed(None, request)
        response = HttpResponse(content_type=fg.content_type)
        fg.write(response, 'utf-8')
    return response.content.decode()

def test_rss2_includes_comments():

    class F(views.Feed):
        title = 'T'
        link = '/'

        def items(self):
            return [Item(1)]

        def item_comments(self, item):
            return item.get_absolute_url() + 'comments'
    content = _render_feed(F())
    assert '/items/1/comments' in content

def test_atom_includes_comments():

    class F(views.Feed):
        feed_type = feedgenerator.Atom1Feed
        title = 'T'
        link = '/'

        def items(self):
            return [Item(2)]

        def item_comments(self, item):
            return item.get_absolute_url() + 'comments'
    content = _render_feed(F())
    assert '/items/2/comments' in content

def test_rss091_includes_comments():

    class F(views.Feed):
        feed_type = feedgenerator.RssUserland091Feed
        title = 'T'
        link = '/'

        def items(self):
            return [Item(3)]

        def item_comments(self, item):
            return item.get_absolute_url() + 'comments'
    content = _render_feed(F())
    assert '/items/3/comments' in content

def test_guid_permalink_true_includes_comments():

    class F(views.Feed):
        title = 'T'
        link = '/'

        def items(self):
            return [Item(4)]

        def item_comments(self, item):
            return item.get_absolute_url() + 'comments'

        def item_guid_is_permalink(self, item):
            return True
    content = _render_feed(F())
    assert '/items/4/comments' in content

def test_guid_permalink_false_includes_comments():

    class F(views.Feed):
        title = 'T'
        link = '/'

        def items(self):
            return [Item(5)]

        def item_comments(self, item):
            return item.get_absolute_url() + 'comments'

        def item_guid(self, item):
            return str(item.pk)

        def item_guid_is_permalink(self, item):
            return False
    content = _render_feed(F())
    assert '/items/5/comments' in content

def test_author_name_branch_includes_comments():

    class F(views.Feed):
        title = 'T'
        link = '/'

        def items(self):
            return [Item(6)]
        item_author_name = 'Author X'
        item_author_email = 'x@example.com'
        item_author_link = 'http://example.com'

        def item_comments(self, item):
            return item.get_absolute_url() + 'comments'
    content = _render_feed(F())
    assert '/items/6/comments' in content

def test_naive_pubdate_is_made_aware_and_includes_comments():

    class F(views.Feed):
        feed_type = feedgenerator.Atom1Feed
        title = 'T'
        link = '/'

        def items(self):
            return [Item(7)]

        def item_pubdate(self, item):
            return datetime.datetime(2020, 1, 1, 12, 0, 0)

        def item_comments(self, item):
            return item.get_absolute_url() + 'comments'
    content = _render_feed(F())
    assert '/items/7/comments' in content

def test_naive_updateddate_is_made_aware_and_includes_comments():

    class F(views.Feed):
        feed_type = feedgenerator.Atom1Feed
        title = 'T'
        link = '/'

        def items(self):
            return [Item(8)]

        def item_updateddate(self, item):
            return datetime.datetime(2020, 2, 2, 13, 0, 0)

        def item_comments(self, item):
            return item.get_absolute_url() + 'comments'
    content = _render_feed(F())
    assert '/items/8/comments' in content

def test_enclosure_and_comments_coexist_includes_comments():

    class F(views.Feed):
        title = 'T'
        link = '/'

        def items(self):
            return [Item(9)]

        def item_enclosure_url(self, item):
            return 'http://example.com/media.png'

        def item_enclosure_length(self, item):
            return 123

        def item_enclosure_mime_type(self, item):
            return 'image/png'

        def item_comments(self, item):
            return item.get_absolute_url() + 'comments'
    content = _render_feed(F())
    assert '/items/9/comments' in content
    assert 'http://example.com/media.png' in content

def test_custom_feed_url_includes_comments():

    class F(views.Feed):
        feed_type = feedgenerator.Atom1Feed
        title = 'T'
        link = '/'
        feed_url = '/custom/feed/url/'

        def items(self):
            return [Item(10)]

        def item_comments(self, item):
            return item.get_absolute_url() + 'comments'
    content = _render_feed(F())
    assert '/items/10/comments' in content
    assert '/custom/feed/url/' in content

from django.test import TestCase, RequestFactory
from django.http import HttpResponse
from django.utils import feedgenerator
from django.test import TestCase, RequestFactory
from django.http import HttpResponse
from django.utils import feedgenerator
from .feeds import TestRss2Feed, TestRss091Feed, TestAtomFeed, TestLatestFeed, TestNoPubdateFeed, TemplateFeed, TemplateContextFeed, TestFeedUrlFeed, TZAwareDatesFeed, TestSingleEnclosureAtomFeed, TestRss2FeedWithGuidIsPermaLinkTrue
from .models import Entry

class CommentsRenderingTests(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.request = self.factory.get('/')

from types import SimpleNamespace
from unittest.mock import patch
from django.test import RequestFactory
from django.utils import feedgenerator
from django.utils.timezone import now
import datetime
from types import SimpleNamespace
from unittest.mock import patch
from django.test import RequestFactory
from django.utils import feedgenerator
from django.utils.timezone import now
from django.contrib.syndication import views
RF = RequestFactory()

def _make_request(path='/feed/'):
    return RF.get(path)
SITE_PATCH = patch('django.contrib.sites.shortcuts.get_current_site', lambda request: SimpleNamespace(domain='example.com'))

def test_rss2_comments_callable_no_author_name():

    class TestFeed(views.Feed):
        link = '/blog/'

        def items(self):
            return [SimpleItem(1)]

        def item_comments(self, item):
            return 'http://example.com%scomments' % item.get_absolute_url()
    req = _make_request()
    with SITE_PATCH:
        feed = TestFeed()
        feedgen = feed.get_feed(None, req)
        resp = type('R', (), {'content': b'', 'write': lambda self, content, encoding: None})()
        from django.http import HttpResponse
        response = HttpResponse(content_type=feedgen.content_type)
        feedgen.write(response, 'utf-8')
        content = response.content.decode('utf-8')
    assert 'comments' in content
    assert '/items/1/comments' in content

def test_rss2_comments_attribute_no_author_name():

    class TestFeed(views.Feed):
        link = '/blog/'
        item_comments = 'http://example.com/items/42/comments'

        def items(self):
            return [SimpleItem(42)]
    req = _make_request()
    with SITE_PATCH:
        feed = TestFeed()
        feedgen = feed.get_feed(None, req)
        from django.http import HttpResponse
        response = HttpResponse(content_type=feedgen.content_type)
        feedgen.write(response, 'utf-8')
        content = response.content.decode('utf-8')
    assert 'items/42/comments' in content

def test_atom_comments_callable_no_author_name():

    class AtomFeed(views.Feed):
        feed_type = feedgenerator.Atom1Feed
        link = '/atom/'

        def items(self):
            return [SimpleItem(3)]

        def item_comments(self, item):
            return 'http://example.com%s#discuss' % item.get_absolute_url()
    req = _make_request()
    with SITE_PATCH:
        feed = AtomFeed()
        feedgen = feed.get_feed(None, req)
        from django.http import HttpResponse
        response = HttpResponse(content_type=feedgen.content_type)
        feedgen.write(response, 'utf-8')
        content = response.content.decode('utf-8')
    assert '#discuss' in content
    assert '/items/3/' in content

def test_atom_comments_attribute_with_author_name():

    class AtomFeed(views.Feed):
        feed_type = feedgenerator.Atom1Feed
        link = '/atom/'
        item_comments = 'http://example.com/items/77/comments'
        item_author_name = 'Alice'

        def items(self):
            return [SimpleItem(77)]
    req = _make_request()
    with SITE_PATCH:
        feed = AtomFeed()
        feedgen = feed.get_feed(None, req)
        from django.http import HttpResponse
        response = HttpResponse(content_type=feedgen.content_type)
        feedgen.write(response, 'utf-8')
        content = response.content.decode('utf-8')
    assert 'items/77/comments' in content

def test_rss2_item_comments_callable_with_item_arg():

    class TestFeed(views.Feed):
        link = '/blog/'

        def items(self):
            return [SimpleItem(5)]

        def item_comments(self, item):
            return 'http://example.com%sreplies' % item.get_absolute_url()
    req = _make_request()
    with SITE_PATCH:
        feed = TestFeed()
        feedgen = feed.get_feed(None, req)
        from django.http import HttpResponse
        response = HttpResponse(content_type=feedgen.content_type)
        feedgen.write(response, 'utf-8')
        content = response.content.decode('utf-8')
    assert 'replies' in content
    assert '/items/5/' in content

def test_rss2_item_comments_callable_no_args():

    class TestFeed(views.Feed):
        link = '/blog/'

        def items(self):
            return [SimpleItem(6)]

        def item_comments(self):
            return 'http://example.com/static/comments'
    req = _make_request()
    with SITE_PATCH:
        feed = TestFeed()
        feedgen = feed.get_feed(None, req)
        from django.http import HttpResponse
        response = HttpResponse(content_type=feedgen.content_type)
        feedgen.write(response, 'utf-8')
        content = response.content.decode('utf-8')
    assert 'static/comments' in content

def test_rss2_item_comments_none():

    class TestFeed(views.Feed):
        link = '/blog/'

        def items(self):
            return [SimpleItem(7)]

        def item_comments(self, item):
            return None
    req = _make_request()
    with SITE_PATCH:
        feed = TestFeed()
        feedgen = feed.get_feed(None, req)
        from django.http import HttpResponse
        response = HttpResponse(content_type=feedgen.content_type)
        feedgen.write(response, 'utf-8')
        content = response.content.decode('utf-8')
    assert 'comments' not in content or '<comments' not in content

def test_rss2_comments_with_other_item_attributes():

    class TestFeed(views.Feed):
        link = '/blog/'
        item_author_name = 'Bob'

        def items(self):
            return [SimpleItem(8)]

        def item_comments(self, item):
            return 'http://example.com%snotes' % item.get_absolute_url()

        def item_description(self, item):
            return 'desc'
    req = _make_request()
    with SITE_PATCH:
        feed = TestFeed()
        feedgen = feed.get_feed(None, req)
        from django.http import HttpResponse
        response = HttpResponse(content_type=feedgen.content_type)
        feedgen.write(response, 'utf-8')
        content = response.content.decode('utf-8')
    assert 'notes' in content
    assert '/items/8/' in content

def test_rss2_comments_network_path():

    class TestFeed(views.Feed):
        link = '/blog/'

        def items(self):
            return [SimpleItem(9)]

        def item_comments(self, item):
            return '//example.com%scomments' % item.get_absolute_url()
    req = _make_request()
    req.environ['wsgi.url_scheme'] = 'https'
    with SITE_PATCH:
        feed = TestFeed()
        feedgen = feed.get_feed(None, req)
        from django.http import HttpResponse
        response = HttpResponse(content_type=feedgen.content_type)
        feedgen.write(response, 'utf-8')
        content = response.content.decode('utf-8')
    assert 'https://example.com/items/9/comments' in content or 'https:' in content

def test_rss2_comments_with_item_extra_kwargs():

    class TestFeed(views.Feed):
        link = '/blog/'

        def items(self):
            return [SimpleItem(10)]

        def item_comments(self, item):
            return 'http://example.com/items/10/comments'

        def item_extra_kwargs(self, item):
            return {'custom': 'value'}
    req = _make_request()
    with SITE_PATCH:
        feed = TestFeed()
        feedgen = feed.get_feed(None, req)
        from django.http import HttpResponse
        response = HttpResponse(content_type=feedgen.content_type)
        feedgen.write(response, 'utf-8')
        content = response.content.decode('utf-8')
    assert 'items/10/comments' in content

import io
from types import SimpleNamespace
from unittest.mock import patch
from django.contrib.syndication import views
from django.utils import feedgenerator

def _make_item(pk=1):

    class Item:

        def __init__(self, pk):
            self.pk = pk
            from datetime import datetime
            self.published = datetime(2020, 1, 1, 12, 0)
            self.updated = datetime(2020, 1, 2, 13, 0)

        def get_absolute_url(self):
            return '/items/%s/' % self.pk

        def __str__(self):
            return 'Item %s' % self.pk
    return Item(pk)

def _make_request():
    return SimpleNamespace(path='/feed/', is_secure=lambda: False)

def _render_feed_to_string(feedgen):
    buf = io.StringIO()
    feedgen.write(buf, 'utf-8')
    return buf.getvalue()

def test_default_feed_includes_item_comments():

    class MyFeed(views.Feed):

        def items(self):
            return [_make_item(1)]

        def item_link(self, item):
            return item.get_absolute_url()

        def item_comments(self, item):
            return item.get_absolute_url() + '#comments'
    req = _make_request()
    with patch('django.contrib.syndication.views.get_current_site', return_value=SimpleNamespace(domain='example.com')):
        feedgen = MyFeed().get_feed(None, req)
        output = _render_feed_to_string(feedgen)
    assert '/items/1/#comments' in output

def test_atom_feed_includes_item_comments():

    class MyFeed(views.Feed):
        feed_type = feedgenerator.Atom1Feed

        def items(self):
            return [_make_item(2)]

        def item_link(self, item):
            return item.get_absolute_url()

        def item_comments(self, item):
            return 'http://example.com' + item.get_absolute_url() + '#c'
    req = _make_request()
    with patch('django.contrib.syndication.views.get_current_site', return_value=SimpleNamespace(domain='example.com')):
        feedgen = MyFeed().get_feed(None, req)
        output = _render_feed_to_string(feedgen)
    assert 'http://example.com/items/2/#c' in output

def test_rss091_feed_includes_item_comments():

    class MyFeed(views.Feed):
        feed_type = feedgenerator.RssUserland091Feed

        def items(self):
            return [_make_item(3)]

        def item_link(self, item):
            return item.get_absolute_url()

        def item_comments(self, item):
            return item.get_absolute_url() + 'comments'
    req = _make_request()
    with patch('django.contrib.syndication.views.get_current_site', return_value=SimpleNamespace(domain='example.com')):
        feedgen = MyFeed().get_feed(None, req)
        output = _render_feed_to_string(feedgen)
    assert '/items/3/comments' in output

def test_feed_with_item_author_branches_and_comments():

    class MyFeed(views.Feed):

        def items(self):
            return [_make_item(4)]

        def item_link(self, item):
            return item.get_absolute_url()
        item_author_name = 'Author'

        def item_author_email(self, item):
            return 'author@example.com'

        def item_author_link(self, item):
            return 'http://author.example.com/'

        def item_comments(self, item):
            return 'http://comments.example.com/' + str(item.pk)
    req = _make_request()
    with patch('django.contrib.syndication.views.get_current_site', return_value=SimpleNamespace(domain='example.com')):
        feedgen = MyFeed().get_feed(None, req)
        output = _render_feed_to_string(feedgen)
    assert 'http://comments.example.com/4' in output
    assert 'author@example.com' in output or 'author.example.com' in output

def test_feed_without_item_author_name_still_includes_comments():

    class MyFeed(views.Feed):

        def items(self):
            return [_make_item(5)]

        def item_link(self, item):
            return item.get_absolute_url()

        def item_comments(self, item):
            return '/comments/for/%s' % item.pk
    req = _make_request()
    with patch('django.contrib.syndication.views.get_current_site', return_value=SimpleNamespace(domain='example.com')):
        feedgen = MyFeed().get_feed(None, req)
        output = _render_feed_to_string(feedgen)
    assert '/comments/for/5' in output

def test_template_based_feed_includes_item_comments_and_templates_do_not_break():

    class MyFeed(views.Feed):
        title_template = None
        description_template = None

        def items(self):
            return [_make_item(6)]

        def item_title(self, item):
            return 'Title'

        def item_description(self, item):
            return 'Desc'

        def item_link(self, item):
            return item.get_absolute_url()

        def item_comments(self, item):
            return '/templ/comments/%s' % item.pk
    req = _make_request()
    with patch('django.contrib.syndication.views.get_current_site', return_value=SimpleNamespace(domain='example.com')):
        feedgen = MyFeed().get_feed(None, req)
        output = _render_feed_to_string(feedgen)
    assert '/templ/comments/6' in output

def test_naive_pubdate_made_aware_and_comments_present():

    class MyFeed(views.Feed):
        feed_type = feedgenerator.Atom1Feed

        def items(self):
            return [_make_item(7)]

        def item_link(self, item):
            return item.get_absolute_url()

        def item_pubdate(self, item):
            return item.published

        def item_comments(self, item):
            return '/naive/comments/%s' % item.pk
    req = _make_request()
    with patch('django.contrib.syndication.views.get_current_site', return_value=SimpleNamespace(domain='example.com')):
        feedgen = MyFeed().get_feed(None, req)
        output = _render_feed_to_string(feedgen)
    assert '/naive/comments/7' in output

def test_naive_updateddate_made_aware_and_comments_present():

    class MyFeed(views.Feed):
        feed_type = feedgenerator.Atom1Feed

        def items(self):
            return [_make_item(8)]

        def item_link(self, item):
            return item.get_absolute_url()

        def item_updateddate(self, item):
            return item.updated

        def item_comments(self, item):
            return '/updated/comments/%s' % item.pk
    req = _make_request()
    with patch('django.contrib.syndication.views.get_current_site', return_value=SimpleNamespace(domain='example.com')):
        feedgen = MyFeed().get_feed(None, req)
        output = _render_feed_to_string(feedgen)
    assert '/updated/comments/8' in output

def test_feed_with_custom_feed_url_includes_comments():

    class MyFeed(views.Feed):
        feed_url = '/customfeed/'

        def items(self):
            return [_make_item(9)]

        def item_link(self, item):
            return item.get_absolute_url()

        def item_comments(self, item):
            return 'http://c.example.com/' + item.get_absolute_url()
    req = _make_request()
    with patch('django.contrib.syndication.views.get_current_site', return_value=SimpleNamespace(domain='example.com')):
        feedgen = MyFeed().get_feed(None, req)
        output = _render_feed_to_string(feedgen)
    assert 'http://c.example.com//items/9/' in output or 'http://c.example.com/items/9/' in output

def test_custom_feed_generator_includes_comments():

    class MyCustomFeedGen(feedgenerator.Atom1Feed):

        def item_attributes(self, item):
            attrs = super().item_attributes(item)
            attrs['x'] = 'y'
            return attrs

    class MyFeed(views.Feed):
        feed_type = MyCustomFeedGen

        def items(self):
            return [_make_item(10)]

        def item_link(self, item):
            return item.get_absolute_url()

        def item_comments(self, item):
            return 'http://comments.example.com/custom/%s' % item.pk
    req = _make_request()
    with patch('django.contrib.syndication.views.get_current_site', return_value=SimpleNamespace(domain='example.com')):
        feedgen = MyFeed().get_feed(None, req)
        output = _render_feed_to_string(feedgen)
    assert 'http://comments.example.com/custom/10' in output

from types import SimpleNamespace
from unittest.mock import patch
from django.contrib.syndication import views
from django.utils import feedgenerator
from django.http import HttpResponse
import datetime
from io import BytesIO
from types import SimpleNamespace
from unittest.mock import patch
from django.contrib.syndication import views
from django.utils import feedgenerator
from django.http import HttpResponse
import unittest

def render_feed(feedobj):
    """
    Return rendered feed content (str) for a feed instance.
    Patches get_current_site to return a predictable domain.
    """
    request = SimpleNamespace(is_secure=lambda: False, path='/feed/')
    with patch.object(views, 'get_current_site', return_value=SimpleNamespace(domain='example.com')):
        feedgen = feedobj.get_feed(None, request)
        response = HttpResponse(content_type=feedgen.content_type)
        feedgen.write(response, 'utf-8')
    content = response.content.decode('utf-8')
    return content
if __name__ == '__main__':
    unittest.main()