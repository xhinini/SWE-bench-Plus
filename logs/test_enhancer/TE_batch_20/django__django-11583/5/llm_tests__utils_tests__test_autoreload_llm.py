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

from unittest import mock
import sys
import tempfile
import shutil
import types
from pathlib import Path
from unittest import mock
from django.test import SimpleTestCase
from django.utils import autoreload

class ValueErrorPathResolveTests(SimpleTestCase):

    def setUp(self):
        self._dir = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self._dir)
        self.good_dir = Path(self._dir).resolve().absolute()
        self.good_file = (self.good_dir / 'good.py').resolve().absolute()
        self.good_file.parent.mkdir(parents=True, exist_ok=True)
        self.good_file.touch()

    def test_iter_modules_and_files_ignores_valueerror_with_custom_message(self):
        bad = '/tmp/bad_custom_message.py'
        autoreload.iter_modules_and_files.cache_clear()
        with self._patch_resolve_for('bad_custom_message', 'network filesystem error'):
            result = autoreload.iter_modules_and_files((), frozenset([bad]))
        self.assertEqual(result, frozenset())

    def test_iter_modules_and_files_handles_mixed_paths(self):
        bad = '/tmp/bad_mixed.py'
        autoreload.iter_modules_and_files.cache_clear()
        extra = frozenset([str(self.good_file), bad])
        with self._patch_resolve_for('bad_mixed', 'some VFS error'):
            result = autoreload.iter_modules_and_files((), extra)
        self.assertIn(self.good_file.resolve(), result)
        self.assertEqual(len(result), 1)

    def test_iter_modules_and_files_ignores_valueerror_on_module_origin(self):
        origin_path = '/tmp/origin_bad.py'
        spec = types.SimpleNamespace(has_location=True, loader=mock.Mock(), origin=origin_path)
        module = types.ModuleType('fake_mod')
        module.__spec__ = spec
        autoreload.iter_modules_and_files.cache_clear()
        with self._patch_resolve_for('origin_bad', 'network error on resolve'):
            result = autoreload.iter_modules_and_files((module,), frozenset())
        self.assertEqual(result, frozenset())

    def test_iter_modules_and_files_with_path_objects_raises_no_exception(self):
        bad_path_obj = Path('/tmp/path_obj_bad.py')
        autoreload.iter_modules_and_files.cache_clear()
        with self._patch_resolve_for('path_obj_bad', 'path object VFS error'):
            result = autoreload.iter_modules_and_files((), frozenset([bad_path_obj]))
        self.assertEqual(result, frozenset())

    def test_iter_modules_and_files_cache_is_cleared_and_ignores_valueerror(self):
        bad = '/tmp/cache_bad.py'
        autoreload.iter_modules_and_files.cache_clear()
        with self._patch_resolve_for('cache_bad', 'cache related VFS error'):
            first = autoreload.iter_modules_and_files((), frozenset([bad]))
            second = autoreload.iter_modules_and_files((), frozenset([bad]))
        self.assertEqual(first, frozenset())
        self.assertEqual(second, frozenset())

from pathlib import Path
import sys
import tempfile
import shutil
from unittest import mock
from pathlib import Path
import sys
import tempfile
import shutil
from unittest import mock
from django.test import SimpleTestCase
from django.utils import autoreload

class ValueErrorResolveTests(SimpleTestCase):

    def setUp(self):
        try:
            autoreload.iter_modules_and_files.cache_clear()
        except Exception:
            pass

    def _make_temp_file(self):
        td = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, td)
        p = Path(td) / 'good.py'
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text('')
        return p
if __name__ == '__main__':
    import unittest
    unittest.main()