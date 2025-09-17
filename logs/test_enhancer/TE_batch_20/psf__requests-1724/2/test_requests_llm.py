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