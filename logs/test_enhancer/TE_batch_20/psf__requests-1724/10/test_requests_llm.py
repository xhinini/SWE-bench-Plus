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