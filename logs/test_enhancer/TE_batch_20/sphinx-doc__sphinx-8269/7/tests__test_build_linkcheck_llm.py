from unittest import mock
import pytest
import pytest
from unittest import mock
NON_HTML_CONTENT_TYPES = ['application/octet-stream', 'text/plain', 'application/json', None, 'text/xml', 'TEXT/PLAIN', 'application/octet-stream; charset=binary', 'image/png', 'audio/mpeg', 'application/x-www-form-urlencoded']