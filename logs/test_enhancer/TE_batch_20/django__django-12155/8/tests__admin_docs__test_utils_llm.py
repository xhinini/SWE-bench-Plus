import unittest
import re
import inspect
from django.contrib.admindocs.utils import docutils_is_available, parse_docstring, parse_rst
from django.test.utils import captured_stderr
from .tests import AdminDocsSimpleTestCase