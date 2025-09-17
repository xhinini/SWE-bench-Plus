import unittest
import re
from inspect import cleandoc
from django.contrib.admindocs.utils import parse_docstring

class ParseDocstringCleandocTests(unittest.TestCase):

    def test_trailing_and_leading_whitespace_lines(self):
        doc = '\n\n    Title surrounded by blank lines\n\n    Body\n\nx: y\n'
        self._assert_parse(doc)