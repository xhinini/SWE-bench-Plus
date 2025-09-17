import os
import io
import requests
import pytest
from requests.compat import urljoin
from requests import Request, Session
import os
import io
import requests
import pytest
from requests.compat import urljoin
from requests import Request, Session
HTTPBIN = os.environ.get('HTTPBIN_URL', 'http://httpbin.org/').rstrip('/') + '/'