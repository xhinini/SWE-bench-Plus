from types import SimpleNamespace
import pytest
from unittest import mock
import sphinx.builders.linkcheck as linkcheck
from types import SimpleNamespace
URL_A = 'https://www.google.com/#top'
URL_B = 'http://www.sphinx-doc.org/en/1.7/intro.html#does-not-exist'
NON_HTML_CONTENT_TYPES = ['application/octet-stream', 'application/pdf', 'text/plain', 'image/png', '']