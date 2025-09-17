import pytest
import requests
from requests.models import PreparedRequest
from requests import Session

def test_session_request_non_ascii_method_prepared():
    s = Session()
    captured = {}
    s.send = _make_send_stub(captured).__get__(s, Session)
    resp = s.request(method='pÖst', url='http://example.com/', allow_redirects=False)
    assert isinstance(resp.request.method, str)
    assert resp.request.method == 'PÖST'
    assert captured.get('request') is resp.request

def test_session_request_with_custom_method_object():
    s = Session()
    captured = {}
    s.send = _make_send_stub(captured).__get__(s, Session)
    method_obj = MethodObj('post')
    resp = s.request(method=method_obj, url='http://example.com/', allow_redirects=False)
    assert isinstance(resp.request.method, str)
    assert resp.request.method == 'POST'
    assert captured.get('request') is resp.request

import os
import requests
import unittest
import os
import unittest
import requests
HTTPBIN = os.environ.get('HTTPBIN_URL', 'http://httpbin.org/')
HTTPBIN = HTTPBIN.rstrip('/') + '/'

class TestNonASCIIHTTPMethods(unittest.TestCase):

    def test_Request_prepare_accepts_non_ascii_method(self):
        req = requests.Request(method=u'PÖST', url=httpbin('anything'))
        prepared = req.prepare()
        assert prepared.method == 'PÖST'

    def test_Session_prepare_request_accepts_non_ascii_method(self):
        s = requests.Session()
        req = requests.Request(method=u'PÖST', url=httpbin('anything'))
        prepared = s.prepare_request(req)
        assert prepared.method == 'PÖST'

None
import unittest
import requests
from requests.models import PreparedRequest, Request
from requests.compat import urljoin, str as compat_str
import os
HTTPBIN = os.environ.get('HTTPBIN_URL', 'http://httpbin.org/')
HTTPBIN = HTTPBIN.rstrip('/') + '/'

class NonAsciiMethodTests(unittest.TestCase):

    def test_request_object_prepare_accepts_nonascii_method(self):
        method = u'PÖST'
        r = Request(method=method, url=httpbin('get'))
        resp_prepared = self.assert_no_value_error_for_method(method, r.prepare)
        self.assertTrue(isinstance(resp_prepared, PreparedRequest))

    def test_session_prepare_request_accepts_nonascii_method(self):
        method = u'PÖST'
        s = requests.Session()
        req = Request(method=method, url=httpbin('get'))
        prepared = self.assert_no_value_error_for_method(method, s.prepare_request, req)
        self.assertTrue(isinstance(prepared, PreparedRequest))

    def test_preparedrequest_prepare_nonascii_method_via_upper(self):
        method = u'PÖST'
        r = Request(method=method, url=httpbin('get'))
        s = requests.Session()
        prepared = self.assert_no_value_error_for_method(method, s.prepare_request, r)
        self.assertTrue(isinstance(prepared, PreparedRequest))
if __name__ == '__main__':
    unittest.main()

import os
import unittest
import requests
from requests.compat import urljoin
HTTPBIN = os.environ.get('HTTPBIN_URL', 'http://httpbin.org/')
HTTPBIN = HTTPBIN.rstrip('/') + '/'

class TestMethodCoercion(unittest.TestCase):

    def test_requests_request_with_method_object_get(self):
        m = MethodLike('GET')
        r = requests.request(method=m, url=httpbin('get'))
        assert r.status_code == 200
        assert isinstance(r.request.method, str)
        assert r.request.method == 'GET'

    def test_session_request_with_method_object_head(self):
        s = requests.Session()
        m = MethodLike('head')
        r = s.request(method=m, url=httpbin('head'))
        assert r.status_code == 200
        assert isinstance(r.request.method, str)
        assert r.request.method == 'HEAD'

import unittest
from requests.models import PreparedRequest
from requests import Request, Session

class TestNonAsciiMethodHandling(unittest.TestCase):

    def test_request_prepare_allows_non_ascii_method_str(self):
        r = Request('PÖST', 'http://example.com/')
        p = r.prepare()
        self.assertEqual(p.method, 'PÖST'.upper())

    def test_request_prepare_allows_non_ascii_method_unicode(self):
        r = Request(u'Pöst', 'http://example.com/')
        p = r.prepare()
        self.assertEqual(p.method, u'Pöst'.upper())

    def test_session_prepare_request_allows_non_ascii_method_str(self):
        s = Session()
        r = Request('PÖST', 'http://example.com/')
        p = s.prepare_request(r)
        self.assertEqual(p.method, 'PÖST'.upper())

    def test_session_prepare_request_allows_non_ascii_method_unicode(self):
        s = Session()
        r = Request(u'Pöst', 'http://example.com/')
        p = s.prepare_request(r)
        self.assertEqual(p.method, u'Pöst'.upper())
if __name__ == '__main__':
    unittest.main()

import pytest
import os
import pytest
import requests
from requests.compat import urljoin
HTTPBIN = os.environ.get('HTTPBIN_URL', 'http://httpbin.org/')
HTTPBIN = HTTPBIN.rstrip('/') + '/'

def test_custom_object_str_returns_ascii():

    class M:

        def __str__(self):
            return 'POST'
    r = _safe_request(M())
    assert hasattr(r, 'status_code') and isinstance(r.status_code, int)

import requests
from requests import Request, Session
from requests.models import PreparedRequest
import unittest
import requests
from requests import Request, Session
from requests.models import PreparedRequest

class TestMethodNormalization(unittest.TestCase):

    def test_custom_method_object_in_session_request(self):
        s = DummySession()
        method_obj = MethodLike('post')
        resp = s.request(method=method_obj, url='http://example.com/', cookies={})
        assert hasattr(s, 'sent_request')
        assert s.sent_request.method == 'POST'
        assert resp.status_code == 200

    def test_requests_request_with_custom_method_object_via_session(self):
        s = DummySession()
        method_obj = MethodLike('options')
        resp = s.request(method=method_obj, url='http://example.com/', cookies={})
        assert s.sent_request.method == 'OPTIONS'
        assert resp.status_code == 200

    def test_non_ascii_method_does_not_raise_in_session_request(self):
        s = DummySession()
        non_ascii = u'PÖST'
        resp = s.request(method=non_ascii, url='http://example.com/', cookies={})
        assert s.sent_request.method == non_ascii.upper()
        assert resp.status_code == 200

    def test_request_with_int_like_object_method(self):

        class IntLikeMethod(object):

            def __str__(self):
                return 'post'
        s = DummySession()
        s.request(method=IntLikeMethod(), url='http://example.com/', cookies={})
        assert s.sent_request.method == 'POST'
if __name__ == '__main__':
    unittest.main()

import unittest
import requests

class TestNonASCIIMethods(unittest.TestCase):

    def test_prepare_accepts_latin1_nonascii_method(self):
        method = u'PÖST'
        r = requests.Request(method=method, url='http://example.com/')
        p = r.prepare()
        self.assertEqual(p.method, method.upper())

    def test_prepare_accepts_cyrillic_nonascii_method(self):
        method = u'ПОСТ'
        r = requests.Request(method=method, url='http://example.com/')
        p = r.prepare()
        self.assertEqual(p.method, method.upper())

    def test_prepare_accepts_emoji_in_method(self):
        method = u'Pὤ2ST'
        r = requests.Request(method=method, url='http://example.com/')
        p = r.prepare()
        self.assertEqual(p.method, method.upper())

    def test_prepare_accepts_hebrew_method(self):
        method = u'הפוסט'
        r = requests.Request(method=method, url='http://example.com/')
        p = r.prepare()
        self.assertEqual(p.method, method.upper())

    def test_session_prepare_request_with_nonascii_method(self):
        method = u'PÖST'
        req = requests.Request(method=method, url='http://example.com/')
        s = requests.Session()
        p = s.prepare_request(req)
        self.assertEqual(p.method, method.upper())

    def test_request_with_method_subclass_of_str_nonascii(self):

        class MyStr(str):
            pass
        method = MyStr(u'PÖST')
        r = requests.Request(method=method, url='http://example.com/')
        p = r.prepare()
        self.assertEqual(p.method, method.upper())

    def test_prepare_accepts_combining_mark_in_method(self):
        method = u'P' + u'O' + u'̈' + u'ST'
        r = requests.Request(method=method, url='http://example.com/')
        p = r.prepare()
        self.assertEqual(p.method, method.upper())

    def test_prepare_accepts_long_nonascii_method(self):
        method = u'M' + u'Ö' * 50
        r = requests.Request(method=method, url='http://example.com/')
        p = r.prepare()
        self.assertEqual(p.method, method.upper())

    def test_prepare_accepts_mixed_ascii_and_nonascii_method(self):
        method = u'PRE' + u'Ö' + u'POST'
        r = requests.Request(method=method, url='http://example.com/')
        p = r.prepare()
        self.assertEqual(p.method, method.upper())
if __name__ == '__main__':
    unittest.main()

import os
import unittest
import requests
from requests.compat import urljoin
HTTPBIN = os.environ.get('HTTPBIN_URL', 'http://httpbin.org/')
HTTPBIN = HTTPBIN.rstrip('/') + '/'

class TestNonASCIIMethods(unittest.TestCase):

    def test_prepare_does_not_raise_on_non_ascii_method(self):
        req = requests.Request(method='PÖST', url=httpbin('anything'))
        prep = req.prepare()
        assert prep.method == 'PÖST'

    def test_session_prepare_request_works(self):
        s = requests.Session()
        req = requests.Request(method='pöst', url=httpbin('anything'))
        prep = s.prepare_request(req)
        assert isinstance(prep, requests.PreparedRequest)
        assert prep.method == 'PÖST'

    def test_prepared_request_method_property(self):
        req = requests.Request(method='pöst', url=httpbin('anything'))
        prep = req.prepare()
        assert prep.method == 'PÖST'

import pytest
import requests
from requests.models import PreparedRequest, Request
from requests.sessions import Session
from requests.cookies import RequestsCookieJar
from requests import Response

def test_request_prepare_accepts_non_ascii_method():
    r = Request(method=u'PÖST', url='http://example.com/', headers=None, files=None, data=None, params=None, auth=None, cookies=None, hooks=None)
    prep = r.prepare()
    assert prep.method == u'PÖST'.upper()

def test_session_prepare_request_accepts_non_ascii_method():
    s = Session()
    r = Request(method=u'PÖST', url='http://example.com/', headers={'X-Test': 'yes'})
    prep = s.prepare_request(r)
    assert prep.method == u'PÖST'.upper()
    assert prep.headers.get('X-Test') == 'yes'

def test_session_request_with_monkeypatched_send_accepts_non_ascii_method():
    s = Session()

    def fake_send(prepared_request, **kwargs):
        assert prepared_request.method == u'PÖST'.upper()
        resp = Response()
        resp.status_code = 200
        return resp
    s.send = fake_send
    resp = s.request(method=u'PÖST', url='http://example.com/')
    assert isinstance(resp, Response)
    assert resp.status_code == 200

def test_request_prepare_accepts_lowercase_non_ascii_method_and_upcases():
    r = Request(method=u'pöst', url='http://example.com/')
    prep = r.prepare()
    assert prep.method == u'pöst'.upper()
    assert prep.method == u'PÖST'

def test_session_prepare_preserves_headers_when_method_is_non_ascii():
    s = Session()
    r = Request(method=u'PÖST', url='http://example.com/', headers={'X-Foo': 'bar'})
    prep = s.prepare_request(r)
    assert prep.headers.get('X-Foo') == 'bar'
    assert prep.method == u'PÖST'.upper()

def test_session_request_accepts_non_ascii_method_when_send_is_bound_method_replacement():
    s = Session()

    def fake_send_bound(prepared_request, **kwargs):
        assert prepared_request.method == u'PÖST'.upper()
        resp = Response()
        resp.status_code = 204
        return resp
    s.send = fake_send_bound
    resp = s.request(method=u'PÖST', url='http://example.com/')
    assert resp.status_code == 204

def test_request_prepare_accepts_subclass_of_str_method():

    class MyStr(str):
        pass
    m = MyStr(u'PÖST')
    r = Request(method=m, url='http://example.com/')
    prep = r.prepare()
    assert isinstance(m, str)
    assert prep.method == u'PÖST'.upper()

import os
from requests.compat import urljoin
import requests
import pytest
HTTPBIN = os.environ.get('HTTPBIN_URL', 'http://httpbin.org/')
HTTPBIN = HTTPBIN.rstrip('/') + '/'

def test_request_prepare_accepts_non_ascii_method_and_normalizes():
    method = u'pöst'
    expected = method.upper()
    req = requests.Request(method=method, url=httpbin('anything'))
    p = req.prepare()
    assert p.method == expected

def test_prepare_request_via_session_preserves_non_ascii_method_uppercase():
    method = u'füNky'
    expected = method.upper()
    s = requests.Session()
    req = requests.Request(method=method, url=httpbin('anything'))
    p = s.prepare_request(req)
    assert p.method == expected

def test_lowercase_non_ascii_method_is_uppercased_by_prepare():
    method = u'pöst'
    expected = method.upper()
    req = requests.Request(method=method, url=httpbin('anything'))
    p = req.prepare()
    assert p.method == expected

# No new imports required beyond what's in the test file.
# -*- coding: utf-8 -*-
import unittest
import requests
from requests import Session, Request


class TestNonAsciiMethodHandling(unittest.TestCase):
    def test_prepare_request_accepts_non_ascii_method(self):
        r = Request(method=u'PÖST', url='http://example.com/')
        p = r.prepare()
        assert p.method == u'PÖST'.upper()
        assert isinstance(p.method, str)

    def test_prepare_request_accepts_lowercase_non_ascii_method(self):
        r = Request(method=u'pöst', url='http://example.com/')
        p = r.prepare()
        assert p.method == u'pöst'.upper()
        assert isinstance(p.method, str)

    def test_session_prepare_request_accepts_non_ascii_method(self):
        s = Session()
        req = Request(method=u'PÖST', url='http://example.com/')
        p = s.prepare_request(req)
        assert p.method == u'PÖST'.upper()
        assert isinstance(p.method, str)

    def test_session_request_with_stub_send_accepts_non_ascii_method(self):
        s = Session()

        # stub send to avoid network I/O; return a Response carrying the prepared request
        def fake_send(request, **kwargs):
            resp = requests.Response()
            resp.status_code = 200
            resp.request = request
            return resp
        s.send = fake_send

        resp = s.request(method=u'PÖST', url='http://example.com/')
        assert resp.request.method == u'PÖST'.upper()
        assert isinstance(resp.request.method, str)

    def test_request_prepare_returns_builtin_str_type(self):
        r = Request(method=u'PÖST', url='http://example.com/')
        p = r.prepare()
        # ensure the prepared request method is a native str
        assert type(p.method) is str

    def test_prepared_request_from_session_preserves_uppercase(self):
        s = Session()
        req = Request(method=u'pöst', url='http://example.com/')
        p = s.prepare_request(req)
        assert p.method == u'pöst'.upper()

    def test_session_prepare_request_with_accented_method_in_request_obj(self):
        s = Session()
        req = Request(method=u'Crêaté', url='http://example.com/')
        p = s.prepare_request(req)
        assert p.method == u'Crêaté'.upper()

    def test_request_prepare_does_not_raise_for_long_unicode_method(self):
        long_method = u'véryLóngMéthød' * 3
        r = Request(method=long_method, url='http://example.com/')
        p = r.prepare()
        assert p.method == long_method.upper()

    def test_prepare_request_multiple_non_ascii_variants(self):
        variants = [u'PÖST', u'ČŤĚ', u'ñandú', u'αβγ']
        for v in variants:
            r = Request(method=v, url='http://example.com/')
            p = r.prepare()
            assert p.method == v.upper()

    def test_session_request_no_value_error_when_method_is_unicode(self):
        s = Session()

        def fake_send(request, **kwargs):
            resp = requests.Response()
            resp.request = request
            return resp
        s.send = fake_send

        # should not raise; prepared/request method should be uppercased
        resp = s.request(method=u'PÖST', url='http://example.com/')
        assert resp.request.method == u'PÖST'.upper()

from unittest.mock import patch
from requests.models import Response
import unittest
from unittest.mock import patch
from requests import Request, Session, request as requests_request
from requests.models import PreparedRequest, Response

class NonAsciiMethodTests(unittest.TestCase):

    def test_request_prepare_accepts_non_ascii_method(self):
        """Request.prepare should accept non-ASCII method names."""
        req = Request(method=u'PÖST', url='http://example.com/')
        prepared = req.prepare()
        self.assertEqual(prepared.method, u'PÖST'.upper())

    def test_session_prepare_request_accepts_non_ascii_method(self):
        """Session.prepare_request should accept non-ASCII method names."""
        s = Session()
        req = Request(method=u'PÖST', url='http://example.com/')
        prepared = s.prepare_request(req)
        self.assertEqual(prepared.method, u'PÖST'.upper())

    @patch.object(Session, 'send', return_value=Response())
    def test_session_request_accepts_non_ascii_method(self, mock_send):
        """Session.request should accept non-ASCII method names (no send error)."""
        s = Session()
        resp = s.request(method=u'PÖST', url='http://example.com/')
        mock_send.assert_called()
        self.assertIsInstance(resp, Response)

    @patch.object(Session, 'send', return_value=Response())
    def test_requests_top_level_accepts_non_ascii_method(self, mock_send):
        """Top-level requests.request should accept non-ASCII method names."""
        resp = requests_request(method=u'PÖST', url='http://example.com/')
        mock_send.assert_called()
        self.assertIsInstance(resp, Response)

    @patch.object(Session, 'send', return_value=Response())
    def test_session_request_with_custom_object_method(self, mock_send):
        """Session.request should accept custom object methods (no send error)."""

        class MethodObj(object):

            def __str__(self):
                return u'PÖST'
        s = Session()
        resp = s.request(method=MethodObj(), url='http://example.com/')
        mock_send.assert_called()
        self.assertIsInstance(resp, Response)

    @patch.object(Session, 'send', return_value=Response())
    def test_requests_top_level_with_custom_object_method(self, mock_send):
        """Top-level requests.request should accept custom object methods too."""

        class MethodObj(object):

            def __str__(self):
                return u'PÖST'
        resp = requests_request(method=MethodObj(), url='http://example.com/')
        mock_send.assert_called()
        self.assertIsInstance(resp, Response)

import requests
from requests import Request, PreparedRequest
import types
import pytest

def test_request_prepare_accepts_non_ascii_method():
    r = Request(method='PÖST', url='http://example.com/')
    p = r.prepare()
    assert p.method == 'PÖST'

def test_session_prepare_request_accepts_non_ascii_method():
    s = requests.Session()
    req = Request(method='délete', url='http://example.com/')
    prepared = s.prepare_request(req)
    assert prepared.method == 'DÉLETE'

def test_requests_api_accepts_non_ascii_method_monkeypatched_send():
    orig_send = requests.sessions.Session.send
    try:
        captured = {}

        def fake_send(self, request, **kwargs):
            captured['method'] = request.method
            resp = requests.Response()
            resp.status_code = 200
            resp._content = b''
            resp.raw = None
            return resp
        requests.sessions.Session.send = fake_send
        r = requests.request(method='öptions', url='http://example.com/')
        assert captured['method'] == 'ÖPTIONS'
        assert r.status_code == 200
    finally:
        requests.sessions.Session.send = orig_send

def test_session_request_accepts_non_ascii_method_and_passes_to_send():
    s = requests.Session()
    captured = {}

    def fake_send(request, **kwargs):
        captured['method'] = request.method
        resp = requests.Response()
        resp.status_code = 201
        resp._content = b''
        resp.raw = None
        return resp
    s.send = fake_send
    resp = s.request(method='mäke', url='http://example.com/')
    assert captured['method'] == 'MÄKE'
    assert resp.status_code == 201

def test_various_non_ascii_methods_uppercased():
    methods = ['pöst', 'Gèt', 'läunch', 'ÄCK', 'πOST']
    for m in methods:
        r = Request(method=m, url='http://example.com/')
        p = r.prepare()
        assert p.method == m.upper()

def test_session_prepare_preserves_unicode_characters():
    s = requests.Session()
    req = Request(method='ÇuSTOM', url='http://example.com/')
    prepared = s.prepare_request(req)
    assert prepared.method == 'ÇUSTOM'

import unittest
import requests

class MethodHandlingTests(unittest.TestCase):

    def test_request_prepare_accepts_unicode_non_ascii_method(self):
        req = requests.Request(method=u'pöst', url='http://example.com/')
        prep = req.prepare()
        self.assertEqual(prep.method, u'PÖST')

    def test_session_prepare_accepts_unicode_non_ascii_method(self):
        s = requests.Session()
        req = requests.Request(method=u'pöst', url='http://example.com/')
        prep = s.prepare_request(req)
        self.assertEqual(prep.method, u'PÖST')

    def test_session_request_accepts_unicode_non_ascii_method_with_fake_send(self):
        s = requests.Session()

        def fake_send(prepared, **kwargs):
            resp = requests.Response()
            resp.status_code = 200
            resp.request = prepared
            resp.raw = None
            resp.history = []
            return resp
        s.send = fake_send
        r = s.request(method=u'pöst', url='http://example.com/', allow_redirects=False)
        self.assertEqual(r.request.method, u'PÖST')

    def test_session_request_accepts_custom_method_object(self):
        s = requests.Session()

        def fake_send(prepared, **kwargs):
            resp = requests.Response()
            resp.status_code = 200
            resp.request = prepared
            resp.raw = None
            resp.history = []
            return resp
        s.send = fake_send
        method_obj = MethodLike('post')
        r = s.request(method=method_obj, url='http://example.com/', allow_redirects=False)
        self.assertEqual(r.request.method, 'POST')

    def test_request_prepare_with_bytes_method_does_not_raise(self):
        req = requests.Request(method=b'POST', url='http://example.com/')
        prep = req.prepare()
        self.assertEqual(prep.method, b'POST')

    def test_prepare_method_returns_str_type_for_unicode_inputs(self):
        req = requests.Request(method=u'pöst', url='http://example.com/')
        prep = req.prepare()
        self.assertIsInstance(prep.method, str)
if __name__ == '__main__':
    unittest.main()