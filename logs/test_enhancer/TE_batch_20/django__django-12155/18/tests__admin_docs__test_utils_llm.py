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

None
import unittest
import inspect
import importlib

from django.contrib.admindocs import utils, views

class AdminDocsTrimDocstringCleandocTests(unittest.TestCase):
    def test_trim_docstring_not_in_utils_hasattr(self):
        # Expect utils.trim_docstring to have been removed in the fixed version.
        self.assertFalse(hasattr(utils, 'trim_docstring'),
                         "utils.trim_docstring should be removed in the patched version.")

    def test_getattr_raises_for_trim_docstring(self):
        # getattr should raise AttributeError when trim_docstring is absent.
        with self.assertRaises(AttributeError):
            # getattr will raise AttributeError if attribute is absent.
            getattr(utils, 'trim_docstring')

    def test_trim_docstring_not_in_dir(self):
        # 'trim_docstring' should not be present in dir(utils).
        self.assertNotIn('trim_docstring', dir(utils))

    def test_views_has_cleandoc_attribute(self):
        # The fixed views module imports cleandoc at module level.
        self.assertTrue(hasattr(views, 'cleandoc'),
                        "views should have 'cleandoc' imported at module level.")

    def test_views_cleandoc_is_callable(self):
        # cleandoc should be the callable from inspect.
        self.assertTrue(callable(getattr(views, 'cleandoc', None)))

    def test_views_cleandoc_is_inspect_cleandoc(self):
        # The imported cleandoc in views should be the same as inspect.cleandoc
        self.assertIs(getattr(views, 'cleandoc', None), inspect.cleandoc)

    def test_combined_utils_views_state(self):
        # Combined assertion: utils must not expose trim_docstring and views must expose cleandoc.
        self.assertFalse(hasattr(utils, 'trim_docstring'))
        self.assertTrue(hasattr(views, 'cleandoc'))

    def test_from_import_trim_docstring_raises(self):
        # Using a from-import for trim_docstring should fail when the symbol is removed.
        with self.assertRaises(ImportError):
            # This executes the from-import at runtime; if trim_docstring is gone,
            # Python will raise ImportError.
            exec("from django.contrib.admindocs.utils import trim_docstring", {})

    def test_cleandoc_in_views_globals(self):
        # cleandoc should be present in the views module's globals().
        self.assertIn('cleandoc', vars(views))

    def test_trim_docstring_absent_everywhere(self):
        # Confirm trim_docstring does not appear anywhere in the utils namespace.
        names = [n for n in dir(utils) if n == 'trim_docstring']
        self.assertEqual(names, [])

if __name__ == "__main__":
    unittest.main()

import unittest
from django.contrib.admindocs.utils import parse_docstring

def make_doc(s1, s2):
    """
    Compose a docstring with s1 leading spaces on the title line and s2 on the
    body line, separated by a blank line (as expected by parse_docstring).
    """
    return f"{' ' * s1}Title\n\n{' ' * s2}Body\n"
if __name__ == '__main__':
    unittest.main()

import re
from inspect import cleandoc
import unittest
import re
from inspect import cleandoc
from django.contrib.admindocs.utils import parse_docstring

class ParseDocstringCleandocTests(unittest.TestCase):

    def test_with_leading_blank_line_and_extra_indent(self):
        doc = '\n        First line\n    Second line'
        self.assert_matches_cleandoc(doc)

    def test_complex_mixed_indentation_example(self):
        doc = '\n                First (extra indented) line\n            next line with less indent\n\n            another paragraph line\n        '
        self.assert_matches_cleandoc(doc)
if __name__ == '__main__':
    unittest.main()

import unittest
from types import SimpleNamespace
from django.contrib import admindocs
from django.contrib.admindocs import utils
import importlib

class ParseDocstringCleandocTests(unittest.TestCase):

    def setUp(self):
        importlib.reload(utils)

    def test_trim_docstring_removed(self):
        self.assertFalse(hasattr(utils, 'trim_docstring'), 'utils.trim_docstring should have been removed in favor of inspect.cleandoc')

    def _install_and_count_cleandoc(self):
        called = SimpleNamespace(count=0)
        original = getattr(utils, 'cleandoc', None)

        def fake_cleandoc(s):
            called.count += 1
            return s
        setattr(utils, 'cleandoc', fake_cleandoc)
        return (called, original)

    def test_parse_docstring_uses_cleandoc_simple(self):
        called, original = self._install_and_count_cleandoc()
        try:
            utils.parse_docstring('Title\n\n    Body')
            self.assertGreater(called.count, 0, 'parse_docstring should call utils.cleandoc')
        finally:
            self._restore_cleandoc(original)

    def test_parse_docstring_uses_cleandoc_multiline(self):
        called, original = self._install_and_count_cleandoc()
        try:
            utils.parse_docstring('First line\n\n    Indented line\n\n    Another paragraph')
            self.assertGreater(called.count, 0)
        finally:
            self._restore_cleandoc(original)

    def test_parse_docstring_uses_cleandoc_with_leading_newline(self):
        called, original = self._install_and_count_cleandoc()
        try:
            utils.parse_docstring('\n    leading\n    indentation\n')
            self.assertGreater(called.count, 0)
        finally:
            self._restore_cleandoc(original)

    def test_parse_docstring_uses_cleandoc_with_tabs(self):
        called, original = self._install_and_count_cleandoc()
        try:
            utils.parse_docstring('Title\n\n\tTabbed line\n\t\tMore')
            self.assertGreater(called.count, 0)
        finally:
            self._restore_cleandoc(original)

    def test_parse_docstring_uses_cleandoc_with_unicode(self):
        called, original = self._install_and_count_cleandoc()
        try:
            utils.parse_docstring('Títle\n\n    Lîné with únîcødé')
            self.assertGreater(called.count, 0)
        finally:
            self._restore_cleandoc(original)

    def test_parse_docstring_uses_cleandoc_multiple_paragraphs(self):
        called, original = self._install_and_count_cleandoc()
        try:
            utils.parse_docstring('One\n\n    Two\n\n    Three\n\nFour')
            self.assertGreater(called.count, 0)
        finally:
            self._restore_cleandoc(original)

    def test_parse_docstring_uses_cleandoc_when_metadata_present(self):
        called, original = self._install_and_count_cleandoc()
        try:
            utils.parse_docstring('Title\n\n    Body\n\nkey: value')
            self.assertGreater(called.count, 0)
        finally:
            self._restore_cleandoc(original)

    def test_parse_docstring_uses_cleandoc_when_only_body(self):
        called, original = self._install_and_count_cleandoc()
        try:
            utils.parse_docstring('Single paragraph with\n    indented continuation')
            self.assertGreater(called.count, 0)
        finally:
            self._restore_cleandoc(original)

    def test_parse_docstring_uses_cleandoc_complex_indentation(self):
        called, original = self._install_and_count_cleandoc()
        try:
            doc = 'Summary line\n\n    - bullet one\n        - nested\n    - bullet two\n'
            utils.parse_docstring(doc)
            self.assertGreater(called.count, 0)
        finally:
            self._restore_cleandoc(original)
if __name__ == '__main__':
    unittest.main()

from django.contrib.admindocs import utils
from django.contrib.admindocs.utils import parse_docstring
import unittest
from django.contrib.admindocs import utils
from django.contrib.admindocs.utils import parse_docstring

class ParseDocstringRegressionTests(unittest.TestCase):

    def test_trim_docstring_removed(self):
        self.assertFalse(hasattr(utils, 'trim_docstring'), 'trim_docstring should be removed')
if __name__ == '__main__':
    unittest.main()