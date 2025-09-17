import requests
import os
from requests.compat import urljoin
import pytest
import requests
import os
from requests.compat import urljoin
import pytest
HTTPBIN = os.environ.get('HTTPBIN_URL', 'http://httpbin.org/')
HTTPBIN = HTTPBIN.rstrip('/') + '/'