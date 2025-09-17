import os
import requests
from requests import Request, Session
import pytest
HTTPBIN = os.environ.get('HTTPBIN_URL', 'http://httpbin.org/')
HTTPBIN = HTTPBIN.rstrip('/') + '/'