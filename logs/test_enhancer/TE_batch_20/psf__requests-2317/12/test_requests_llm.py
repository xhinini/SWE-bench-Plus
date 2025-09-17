import os
import requests
import pytest
from requests import Request, PreparedRequest, Session
HTTPBIN = os.environ.get('HTTPBIN_URL', 'http://httpbin.org/')
HTTPBIN = HTTPBIN.rstrip('/') + '/'