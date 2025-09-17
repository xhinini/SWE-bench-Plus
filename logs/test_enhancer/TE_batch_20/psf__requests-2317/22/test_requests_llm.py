import os
import requests
import pytest
from requests.compat import urljoin
from requests.models import PreparedRequest, Request
import os
import requests
import pytest
from requests.compat import urljoin
from requests.models import PreparedRequest, Request
HTTPBIN = os.environ.get('HTTPBIN_URL', 'http://httpbin.org/')
HTTPBIN = HTTPBIN.rstrip('/') + '/'