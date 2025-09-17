import os
import requests
import pytest
from requests.models import Request, PreparedRequest
from requests.compat import urljoin
import os
import requests
import pytest
from requests.models import Request, PreparedRequest
from requests.compat import urljoin
HTTPBIN = os.environ.get('HTTPBIN_URL', 'http://httpbin.org/')
HTTPBIN = HTTPBIN.rstrip('/') + '/'