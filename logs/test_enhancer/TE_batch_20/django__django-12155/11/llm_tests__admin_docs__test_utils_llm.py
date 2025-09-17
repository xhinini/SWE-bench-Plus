import unittest
import re
from inspect import cleandoc
from django.contrib.admindocs.utils import parse_docstring

class ParseDocstringCleandocTests(unittest.TestCase):

    def test_trailing_and_leading_whitespace_lines(self):
        doc = '\n\n    Title surrounded by blank lines\n\n    Body\n\nx: y\n'
        self._assert_parse(doc)

import inspect
from django.contrib.admindocs.utils import parse_docstring, docutils_is_available
from django.test.utils import captured_stderr
from .tests import AdminDocsSimpleTestCase
import unittest
import inspect
from django.contrib.admindocs.utils import parse_docstring, docutils_is_available
from .tests import AdminDocsSimpleTestCase

@unittest.skipUnless(docutils_is_available, 'no docutils installed.')
class ParseDocstringCleandocBehaviorTests(AdminDocsSimpleTestCase):
    """
    Tests to ensure parse_docstring() behaves as if inspect.cleandoc() was used
    to normalize the incoming docstring (the behaviour introduced by the gold patch).
    """

    def test_whitespace_only_docstring_returns_empty(self):
        self.assert_parsed_matches_cleandoc('   \n\t  \n')

from inspect import cleandoc
import unittest
import inspect
from inspect import cleandoc
import importlib
import types
from django.contrib.admindocs import utils as adm_utils
from django.contrib.admindocs import views as adm_views

class AdmindocsUtilsRegressionTests(unittest.TestCase):

    def test_trim_docstring_attribute_removed(self):
        self.assertFalse(hasattr(adm_utils, 'trim_docstring'), 'trim_docstring should have been removed in the fixed version.')

    def test_no_trim_docstring_definition_in_utils_source(self):
        src = inspect.getsource(importlib.import_module('django.contrib.admindocs.utils'))
        self.assertNotIn('def trim_docstring', src, 'utils module should not define trim_docstring in the fixed version.')

    def test_utils_uses_cleandoc(self):
        src = inspect.getsource(importlib.import_module('django.contrib.admindocs.utils'))
        self.assertIn('cleandoc(', src, 'utils.parse_docstring should use cleandoc in the fixed version.')

    def test_views_uses_cleandoc_for_method_verbose(self):
        src = inspect.getsource(importlib.import_module('django.contrib.admindocs.views'))
        self.assertIn('cleandoc(verbose)', src, 'views should use cleandoc(verbose) when formatting model method docstrings.')

    def test_views_does_not_call_utils_trim_docstring(self):
        src = inspect.getsource(importlib.import_module('django.contrib.admindocs.views'))
        self.assertNotIn('utils.trim_docstring', src, 'views must not call utils.trim_docstring in the fixed version.')
if __name__ == '__main__':
    unittest.main()

import re
from inspect import cleandoc
import re
import unittest
from inspect import cleandoc
from django.contrib.admindocs.utils import parse_docstring

def _expected_parse_docstring(docstring):
    """
    Compute expected (title, body, metadata) using inspect.cleandoc and the
    same splitting/metadata parsing rules that parse_docstring should follow.
    """
    if not docstring:
        return ('', '', {})
    cleaned = cleandoc(docstring)
    parts = re.split('\\n{2,}', cleaned)
    title = parts[0]
    if len(parts) == 1:
        return (title, '', {})
    body = parts[1]
    metadata = {}
    if len(parts) >= 3:
        for line in parts[2].splitlines():
            if ':' in line:
                key, val = line.split(':', 1)
                metadata[key.strip()] = val.strip()
    return (title, body, metadata)

from inspect import cleandoc
from django.apps import apps
from django.test import RequestFactory
from django.test.utils import captured_stderr
from django.contrib.admindocs import utils
from django.contrib.admindocs.views import ModelDetailView
from django.contrib.admindocs.utils import docutils_is_available, parse_docstring, parse_rst
from django.db import models
import unittest
from inspect import cleandoc
from django.apps import apps
from django.test import RequestFactory
from django.test.utils import captured_stderr
from django.contrib.admindocs import utils
from django.contrib.admindocs.views import ModelDetailView
from django.contrib.admindocs.utils import docutils_is_available, parse_docstring, parse_rst
from django.db import models
from .tests import AdminDocsSimpleTestCase

@unittest.skipUnless(docutils_is_available, 'no docutils installed.')
class TestAdmindocsParsingAndModelDetail(AdminDocsSimpleTestCase):

    def setUp(self):
        self.rf = RequestFactory()
        self._registered = []

    def tearDown(self):
        for app_label, model_name in self._registered:
            app_models = apps.all_models.get(app_label, {})
            if model_name in app_models:
                del app_models[model_name]
if __name__ == '__main__':
    unittest.main()