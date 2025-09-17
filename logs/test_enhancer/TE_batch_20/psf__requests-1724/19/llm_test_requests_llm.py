import os
import unittest
import requests
from requests.compat import urljoin
HTTPBIN = os.environ.get('HTTPBIN_URL', 'http://httpbin.org/')
HTTPBIN = HTTPBIN.rstrip('/') + '/'
if __name__ == '__main__':
    unittest.main()