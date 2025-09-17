import os
import requests
import pytest
from requests.compat import urljoin
from requests.models import PreparedRequest
from requests import Request
HTTPBIN = os.environ.get('HTTPBIN_URL', 'http://httpbin.org/')
HTTPBIN = HTTPBIN.rstrip('/') + '/'
NON_ASCII_METHOD = u'PÖST'