import requests
import pytest
from requests.models import PreparedRequest
from requests import Request
from requests.compat import urljoin
import os
HTTPBIN = os.environ.get('HTTPBIN_URL', 'http://httpbin.org/')
HTTPBIN = HTTPBIN.rstrip('/') + '/'