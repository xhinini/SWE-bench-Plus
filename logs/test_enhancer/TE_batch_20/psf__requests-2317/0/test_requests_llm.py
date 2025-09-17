import os
import pytest
import requests
from requests.compat import urljoin
from requests.models import PreparedRequest, Request
from requests import Session
HTTPBIN = os.environ.get('HTTPBIN_URL', 'http://httpbin.org/')
HTTPBIN = HTTPBIN.rstrip('/') + '/'