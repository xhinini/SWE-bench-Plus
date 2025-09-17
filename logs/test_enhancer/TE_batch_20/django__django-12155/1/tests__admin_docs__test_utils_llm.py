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