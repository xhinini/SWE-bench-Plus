from docutils import nodes
from unittest import mock
from pathlib import Path
import pytest
from unittest import mock
from docutils import nodes
from pathlib import Path
TEST_URLS = [('https://example.com/page#missing1', 'missing1'), ('https://example.org/page#missing2', 'missing2'), ('https://cdn.example.net/doc.pdf#missing3', 'missing3'), ('http://localhost:8000/path#missing4', 'missing4'), ('https://www.google.com/#top', 'top'), ('http://www.sphinx-doc.org/en/1.7/intro.html#does-not-exist', 'does-not-exist'), ('https://mysite.test/page#nope', 'nope'), ('https://another.test/index.html#noanchor', 'noanchor'), ('https://files.example.com/doc#anchorX', 'anchorX'), ('https://sub.domain.test/path#notfound', 'notfound')]