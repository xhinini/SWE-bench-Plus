from unittest import mock
import tempfile
from django.test import SimpleTestCase
from pathlib import Path
import tempfile
import os
from django.utils import autoreload
from unittest import mock
ORIGINAL_RESOLVE = Path.resolve

class IterModulesAndFilesValueErrorTests(SimpleTestCase):

    def setUp(self):
        autoreload.iter_modules_and_files.cache_clear()

    def tearDown(self):
        autoreload.iter_modules_and_files.cache_clear()

    def test_iter_modules_and_files_ignores_generic_value_error_message(self):
        result = self._call_with_resolve_side_effect('some random error', [str(Path('/tmp/fake_a.py'))])
        self.assertEqual(result, frozenset())

    def test_iter_modules_and_files_ignores_different_message(self):
        result = self._call_with_resolve_side_effect('another message', [str(Path('/tmp/fake_b.py'))])
        self.assertEqual(result, frozenset())

    def test_iter_modules_and_files_rejects_similar_but_not_exact_message_with_trailing_space(self):
        result = self._call_with_resolve_side_effect('embedded null byte ', [str(Path('/tmp/fake_c.py'))])
        self.assertEqual(result, frozenset())

    def test_iter_modules_and_files_handles_empty_message(self):
        result = self._call_with_resolve_side_effect('', [str(Path('/tmp/fake_d.py'))])
        self.assertEqual(result, frozenset())

    def test_iter_modules_and_files_handles_uppercase_message(self):
        result = self._call_with_resolve_side_effect('EMBEDDED NULL BYTE', [str(Path('/tmp/fake_e.py'))])
        self.assertEqual(result, frozenset())

    def test_iter_modules_and_files_handles_embedded_null_with_extra_byte(self):
        result = self._call_with_resolve_side_effect('embedded null byte\\x00', [str(Path('/tmp/fake_f.py'))])
        self.assertEqual(result, frozenset())

    def test_iter_modules_and_files_handles_embedded_null_with_escape(self):
        result = self._call_with_resolve_side_effect('embedded null byte\\0', [str(Path('/tmp/fake_g.py'))])
        self.assertEqual(result, frozenset())

    def test_iter_modules_and_files_handles_value_error_with_null_byte_character(self):
        result = self._call_with_resolve_side_effect('embedded null byte' + '\x00', [str(Path('/tmp/fake_h.py'))])
        self.assertEqual(result, frozenset())

from pathlib import Path
import tempfile
import sys
from unittest import mock
from pathlib import Path
import sys
import tempfile
import os
from unittest import mock
from django.test import SimpleTestCase
from django.test.utils import extend_sys_path
from django.utils import autoreload

class IterModulesAndFilesValueErrorHandlingTests(SimpleTestCase):

    def test_iter_modules_and_files_ignores_valueerror_random_msg(self):
        autoreload.iter_modules_and_files.cache_clear()
        with mock.patch.object(Path, 'resolve', side_effect=ValueError('some random error')):
            result = autoreload.iter_modules_and_files((), frozenset(['badpath']))
        self.assertEqual(result, frozenset())

    def test_iter_modules_and_files_ignores_valueerror_empty_msg(self):
        autoreload.iter_modules_and_files.cache_clear()
        with mock.patch.object(Path, 'resolve', side_effect=ValueError()):
            result = autoreload.iter_modules_and_files((), frozenset(['anotherbad']))
        self.assertEqual(result, frozenset())

    def test_iter_modules_and_files_logs_debug_on_valueerror(self):
        autoreload.iter_modules_and_files.cache_clear()
        with mock.patch.object(Path, 'resolve', side_effect=ValueError('weird fs issue')), mock.patch.object(autoreload.logger, 'debug') as mocked_debug:
            result = autoreload.iter_modules_and_files((), frozenset(['badpath']))
            self.assertEqual(result, frozenset())
            mocked_debug.assert_called()

from unittest import mock
import sys
import tempfile
import types
from pathlib import Path
from django.test import SimpleTestCase
from django.test.utils import extend_sys_path
from django.utils import autoreload
from unittest import mock
import sys
import tempfile
import types
from pathlib import Path
from django.test import SimpleTestCase
from django.test.utils import extend_sys_path
from django.utils import autoreload

class TestValueErrorHandling(SimpleTestCase):

    def setUp(self):
        self.orig_resolve = Path.resolve

    def tearDown(self):
        try:
            autoreload.iter_modules_and_files.cache_clear()
        except Exception:
            pass