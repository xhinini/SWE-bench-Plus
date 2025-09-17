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

from pathlib import Path
import tempfile
import shutil
import sys
import types
from unittest import mock
import sys
import types
import tempfile
import shutil
from importlib import import_module
from pathlib import Path
from unittest import mock
from django.test import SimpleTestCase
from django.utils import autoreload

class ValueErrorPathHandlingTests(SimpleTestCase):

    def setUp(self):
        self._orig_sys_path = list(sys.path)
        self._orig_error_files = list(getattr(autoreload, '_error_files', []))
        autoreload.iter_modules_and_files.cache_clear()
        self.tempdir = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.tempdir)
        self.good_file = Path(self.tempdir) / 'good.py'
        self.good_file.touch()

    def tearDown(self):
        sys.path[:] = self._orig_sys_path
        autoreload._error_files[:] = self._orig_error_files
        autoreload.iter_modules_and_files.cache_clear()

    def test_iter_modules_and_files_ignores_value_error_for_extra_files_string(self):
        with mock.patch('django.utils.autoreload.Path.resolve', side_effect=ValueError('some filesystem error')):
            autoreload.iter_modules_and_files.cache_clear()
            result = autoreload.iter_modules_and_files((), frozenset(['bad/path']))
        self.assertEqual(result, frozenset())

    def test_iter_modules_and_files_ignores_value_error_for_extra_files_path_object(self):
        with mock.patch('django.utils.autoreload.Path.resolve', side_effect=ValueError('another error')):
            autoreload.iter_modules_and_files.cache_clear()
            result = autoreload.iter_modules_and_files((), frozenset([Path('bad/path')]))
        self.assertEqual(result, frozenset())

    def test_iter_modules_and_files_ignores_value_error_from_module_origin(self):
        mod = types.ModuleType('test_bad_origin')

        class FakeSpec:
            has_location = True
            loader = object()
            origin = '/some/bad/origin'
        mod.__spec__ = FakeSpec()
        with mock.patch('django.utils.autoreload.Path.resolve', side_effect=ValueError('origin resolution error')):
            autoreload.iter_modules_and_files.cache_clear()
            result = autoreload.iter_modules_and_files((mod,), frozenset())
        self.assertEqual(result, frozenset())

    def test_iter_all_python_module_files_ignores_value_error_from_error_files(self):
        autoreload._error_files[:] = ['/path/with\x00null']
        with mock.patch('django.utils.autoreload.Path.resolve', side_effect=ValueError('null in path')):
            autoreload.iter_modules_and_files.cache_clear()
            result = list(autoreload.iter_all_python_module_files())
        self.assertEqual(result, [])
if __name__ == '__main__':
    import unittest
    unittest.main()

from pathlib import Path
import sys
import tempfile
import shutil
import types
from unittest import mock
from django.test import SimpleTestCase
from django.utils import autoreload
from pathlib import Path
import sys
import tempfile
import shutil
import types
from unittest import mock
from django.test import SimpleTestCase
from django.utils import autoreload

class ValueErrorResolveTests(SimpleTestCase):

    def setUp(self):
        self._tmpdir = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self._tmpdir)
        self.tmpdir = Path(self._tmpdir).resolve().absolute()
        self.good_file = self.tmpdir / 'good.py'
        self.good_file.touch()
        self._original_resolve = Path.resolve

    def tearDown(self):
        try:
            autoreload.iter_modules_and_files.cache_clear()
        except Exception:
            pass

    def _patch_resolve_raise_on_bad(self, bad_marker='bad_marker'):
        """
        Patch Path.resolve so that it raises ValueError for paths that contain
        the bad_marker in their string representation, and otherwise delegates
        to the original resolve (with strict=False to be permissive).
        """
        original = self._original_resolve

        def fake_resolve(self, strict=True):
            if bad_marker in str(self):
                raise ValueError('simulated filesystem ValueError for %s' % str(self))
            return original(self, strict=False).absolute()
        return mock.patch.object(Path, 'resolve', side_effect=fake_resolve)

from pathlib import Path
import sys
import tempfile
import os
from unittest import mock
from django.test import SimpleTestCase
from django.utils import autoreload
from pathlib import Path
import sys
import tempfile
import os
from unittest import mock
from django.test import SimpleTestCase
from django.utils import autoreload

class ValueErrorHandlingTests(SimpleTestCase):

    def setUp(self):
        autoreload.iter_modules_and_files.cache_clear()
        self.orig_resolve = Path.resolve

    def tearDown(self):
        autoreload.iter_modules_and_files.cache_clear()

from pathlib import Path
import sys
import types
from unittest import mock
from django.test import SimpleTestCase
from django.utils import autoreload
from pathlib import Path
import sys
import types
from unittest import mock
from django.test import SimpleTestCase
from django.utils import autoreload

class ValueErrorPathHandlingTests(SimpleTestCase):

    def tearDown(self):
        autoreload.iter_modules_and_files.cache_clear()

    def test_iter_modules_and_files_swallow_value_error_for_extra_files_string(self):
        bad = 'bad\x00.py'
        with mock.patch.object(Path, 'resolve', side_effect=ValueError('not an embedded null byte')):
            result = autoreload.iter_modules_and_files((), frozenset([bad]))
        self.assertEqual(result, frozenset())

    def test_iter_modules_and_files_swallow_value_error_for_extra_files_pathobj(self):
        bad_path = Path('bad\x00.py')
        with mock.patch.object(Path, 'resolve', side_effect=ValueError('some value error')):
            result = autoreload.iter_modules_and_files((), frozenset([bad_path]))
        self.assertEqual(result, frozenset())

    def test_iter_modules_and_files_swallow_value_error_for_main_module_file_attr(self):
        main = types.ModuleType('__main__')
        main.__file__ = 'main_bad\x00.py'
        with mock.patch.object(Path, 'resolve', side_effect=ValueError('main resolve error')):
            result = autoreload.iter_modules_and_files((main,), frozenset())
        self.assertEqual(result, frozenset())

    def test_iter_modules_and_files_swallow_value_error_for_spec_origin(self):

        class FakeLoader:
            pass
        spec = types.SimpleNamespace(has_location=True, origin='origin_bad\x00.py', loader=FakeLoader())
        module = types.ModuleType('fake_mod')
        module.__spec__ = spec
        with mock.patch.object(Path, 'resolve', side_effect=ValueError('origin resolve error')):
            result = autoreload.iter_modules_and_files((module,), frozenset())
        self.assertEqual(result, frozenset())

    def test_iter_modules_and_files_logs_debug_on_value_error(self):
        bad = 'another_bad\x00'
        with mock.patch.object(Path, 'resolve', side_effect=ValueError('weird error message')):
            with mock.patch.object(autoreload.logger, 'debug') as mocked_debug:
                result = autoreload.iter_modules_and_files((), frozenset([bad]))
        self.assertEqual(result, frozenset())
        self.assertTrue(mocked_debug.called)

    def test_iter_modules_and_files_handles_value_error_with_nonstandard_message(self):
        bad = 'bad_nonstandard\x00'
        with mock.patch.object(Path, 'resolve', side_effect=ValueError('nonstandard message')):
            result = autoreload.iter_modules_and_files((), frozenset([bad]))
        self.assertEqual(result, frozenset())

from unittest import mock
import sys
import types
import tempfile
import os
from pathlib import Path
from django.test import SimpleTestCase
from django.test.utils import extend_sys_path
from django.utils import autoreload

class TestValueErrorHandling(SimpleTestCase):

    def setUp(self):
        try:
            autoreload.iter_modules_and_files.cache_clear()
        except Exception:
            pass
        self.tempdir = tempfile.TemporaryDirectory()
        self.addCleanup(self.tempdir.cleanup)
        self.dirpath = Path(self.tempdir.name).resolve().absolute()

from pathlib import Path
import tempfile
import types
import sys
import os
from unittest import mock
from django.test import SimpleTestCase
from django.test.utils import extend_sys_path
from django.utils import autoreload

class TestValueErrorPathHandling(SimpleTestCase):

    def setUp(self):
        self._tmpdir = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmpdir.cleanup)
        self.valid_dir = Path(self._tmpdir.name).resolve().absolute()
        self.valid_file = self.valid_dir / 'good.py'
        self.valid_file.parent.mkdir(parents=True, exist_ok=True)
        self.valid_file.write_text('# good')

from pathlib import Path
import sys
import tempfile
import types
from unittest import mock
from django.test import SimpleTestCase
from django.utils import autoreload
import os
from pathlib import Path
import sys
import tempfile
import types
from unittest import mock
from django.test import SimpleTestCase
from django.utils import autoreload

class RegressionAutoreloadValueErrorTests(SimpleTestCase):

    def setUp(self):
        try:
            autoreload.iter_modules_and_files.cache_clear()
        except Exception:
            pass

    def _make_bad_path(self):
        return '/tmp/some_network_path_with_null'

import types
from unittest import mock
from unittest import mock
import types
import sys
from pathlib import Path
from django.test import SimpleTestCase
from django.utils import autoreload

class ValueErrorHandlingTests(SimpleTestCase):

    def setUp(self):
        autoreload.iter_modules_and_files.cache_clear()

    def tearDown(self):
        autoreload.iter_modules_and_files.cache_clear()

    def _raise_value_error_on_resolve(self, message='network fs error'):
        return mock.patch.object(Path, 'resolve', side_effect=ValueError(message))

    def test_iter_modules_and_files_ignores_valueerror_for_module_origin(self):
        module = types.ModuleType('test_bad_origin')
        module.__spec__ = types.SimpleNamespace(has_location=True, loader=object(), origin='bad_origin_path')
        with self._raise_value_error_on_resolve('custom message'):
            result = autoreload.iter_modules_and_files((module,), frozenset())
        self.assertEqual(result, frozenset())

    def test_iter_modules_and_files_ignores_valueerror_for_main_module_file(self):
        main_module = types.ModuleType('__main__')
        main_module.__file__ = 'bad_main_path'
        with self._raise_value_error_on_resolve('another message'):
            result = autoreload.iter_modules_and_files((main_module,), frozenset())
        self.assertEqual(result, frozenset())

    def test_iter_modules_and_files_ignores_valueerror_for_extra_file_string(self):
        bad = 'some/bad/path'
        with self._raise_value_error_on_resolve('weird fs error'):
            result = autoreload.iter_modules_and_files((), frozenset([bad]))
        self.assertEqual(result, frozenset())

    def test_iter_modules_and_files_ignores_valueerror_for_extra_file_path(self):
        bad_path = Path('some/bad/path2')
        with self._raise_value_error_on_resolve('different message'):
            result = autoreload.iter_modules_and_files((), frozenset([bad_path]))
        self.assertEqual(result, frozenset())

    def test_iter_all_python_module_files_ignores_valueerror_from_error_files(self):
        with mock.patch.object(autoreload, '_error_files', ['ignored/bad']):
            with self._raise_value_error_on_resolve('network issue'):
                result = autoreload.iter_all_python_module_files()
                self.assertIsInstance(result, frozenset)
                self.assertEqual(result, frozenset())

    def test_iter_modules_and_files_swallow_various_value_error_messages(self):
        module = types.ModuleType('test_various_message')
        module.__spec__ = types.SimpleNamespace(has_location=True, loader=object(), origin='bad_origin_variants')
        for msg in ('foo', 'embedded null byte', 'some other msg'):
            with self.subTest(msg=msg):
                with self._raise_value_error_on_resolve(msg):
                    result = autoreload.iter_modules_and_files((module,), frozenset())
                self.assertEqual(result, frozenset())

    def test_iter_modules_and_files_does_not_raise_on_valueerror_in_combination(self):
        module = types.ModuleType('test_combined')
        module.__spec__ = types.SimpleNamespace(has_location=True, loader=object(), origin='x')
        with self._raise_value_error_on_resolve('combined case'):
            result = autoreload.iter_modules_and_files((module,), frozenset(['y', Path('z')]))
        self.assertEqual(result, frozenset())

from pathlib import Path
import sys
import tempfile
import shutil
from types import ModuleType
from unittest import mock
from django.test import SimpleTestCase
from django.test.utils import extend_sys_path
from django.utils import autoreload

class ResolveValueErrorTests(SimpleTestCase):

    def setUp(self):
        self._td = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self._td)
        self.tempdir = Path(self._td).resolve().absolute()
        self.good_file = self.tempdir / 'good.py'
        self.good_file.touch()
        autoreload.iter_modules_and_files.cache_clear()

    def test_iter_modules_and_files_ignores_value_error_with_arbitrary_message(self):
        bad_path = '/some/bad1/path.py'
        orig_resolve = Path.resolve
        fake = self.fake_resolve_factory(orig_resolve, 'bad1', 'some arbitrary error')
        with mock.patch.object(Path, 'resolve', new=fake):
            result = autoreload.iter_modules_and_files((), frozenset([bad_path]))
        self.assertEqual(result, frozenset())

    def test_iter_modules_and_files_ignores_value_error_with_embedded_null_variation(self):
        bad_path = '/some/bad2/path.py'
        orig_resolve = Path.resolve
        fake = self.fake_resolve_factory(orig_resolve, 'bad2', 'embedded null byte in path')
        with mock.patch.object(Path, 'resolve', new=fake):
            result = autoreload.iter_modules_and_files((), frozenset([bad_path]))
        self.assertEqual(result, frozenset())

    def test_iter_modules_and_files_ignores_value_error_for_module_origin_arbitrary_message(self):
        bad_origin = '/origin/bad3.py'
        module = ModuleType('testmod_bad3')
        spec = type('S', (), {})()
        spec.has_location = True
        spec.origin = bad_origin
        spec.loader = object()
        module.__spec__ = spec
        orig_resolve = Path.resolve
        fake = self.fake_resolve_factory(orig_resolve, 'bad3', 'another message')
        with mock.patch.object(Path, 'resolve', new=fake):
            result = autoreload.iter_modules_and_files((module,), frozenset())
        self.assertEqual(result, frozenset())

    def test_iter_modules_and_files_ignores_multiple_value_errors_and_returns_good_files(self):
        bad_path = '/bad4/file.py'
        orig_resolve = Path.resolve
        fake = self.fake_resolve_factory(orig_resolve, 'bad4', 'bad message 4')
        with mock.patch.object(Path, 'resolve', new=fake):
            result = autoreload.iter_modules_and_files((), frozenset([bad_path, str(self.good_file)]))
        self.assertIn(self.good_file.resolve(), result)

    def test_iter_modules_and_files_handles_multiple_bad_paths(self):
        bad1 = '/multi/badA.py'
        bad2 = '/multi/badB.py'
        orig_resolve = Path.resolve

        def fake_resolve(self, strict=True):
            s = str(self)
            if 'badA' in s:
                raise ValueError('first bad')
            if 'badB' in s:
                raise ValueError('second bad')
            return orig_resolve(self, strict=strict)
        with mock.patch.object(Path, 'resolve', new=fake_resolve):
            result = autoreload.iter_modules_and_files((), frozenset([bad1, bad2]))
        self.assertEqual(result, frozenset())

    def test_iter_modules_and_files_ignores_value_error_when_path_object_passed(self):
        bad_path_obj = Path('/pathobj/bad5.py')
        orig_resolve = Path.resolve
        fake = self.fake_resolve_factory(orig_resolve, 'bad5', 'pathobj error')
        with mock.patch.object(Path, 'resolve', new=fake):
            result = autoreload.iter_modules_and_files((), frozenset([bad_path_obj]))
        self.assertEqual(result, frozenset())
if __name__ == '__main__':
    import unittest
    unittest.main()

import tempfile
import types
import sys
from pathlib import Path
from unittest import mock
from django.test import SimpleTestCase
from django.utils import autoreload

class ValueErrorHandlingTests(SimpleTestCase):

    def setUp(self):
        autoreload.iter_modules_and_files.cache_clear()

from unittest import mock
import tempfile
import types
from pathlib import Path
from django.test import SimpleTestCase
from django.utils import autoreload

class ValueErrorHandlingTests(SimpleTestCase):

    def setUp(self):
        try:
            autoreload.iter_modules_and_files.cache_clear()
        except AttributeError:
            pass

from pathlib import Path
import types
from django.test import SimpleTestCase
from django.test.utils import extend_sys_path
from unittest import mock
import types
import sys
from pathlib import Path
from django.test import SimpleTestCase
from django.test.utils import extend_sys_path
from django.utils import autoreload
from django.utils.autoreload import iter_modules_and_files, sys_path_directories

class ValueErrorResolveTests(SimpleTestCase):

    def setUp(self):
        iter_modules_and_files.cache_clear()

from unittest import mock
import types
from pathlib import Path
from unittest import mock
import types
from pathlib import Path
from django.test import SimpleTestCase
from django.utils import autoreload
import sys

class ValueErrorHandlingTests(SimpleTestCase):

    def setUp(self):
        try:
            autoreload.iter_modules_and_files.cache_clear()
        except AttributeError:
            pass

    def test_iter_modules_and_files_ignores_value_error_from_extra_files(self):
        with mock.patch.object(Path, 'resolve', side_effect=ValueError('some unexpected message')):
            result = autoreload.iter_modules_and_files((), frozenset(['some/bad/path.py']))
        self.assertEqual(result, frozenset())

    def test_iter_modules_and_files_ignores_value_error_from_module_origin(self):
        module = types.ModuleType('test_mod')
        module.__spec__ = types.SimpleNamespace(has_location=True, loader=object(), origin='some/bad/origin.py')
        with mock.patch.object(Path, 'resolve', side_effect=ValueError('module origin boom')):
            result = autoreload.iter_modules_and_files((module,), frozenset())
        self.assertEqual(result, frozenset())

    def test_iter_modules_and_files_returns_good_paths_when_some_raise(self):
        temp = Path(__file__).resolve()

        def resolve_side_effect(self, strict=True):
            if str(self).endswith('good.py'):
                return temp
            raise ValueError('bad path')
        with mock.patch.object(Path, 'resolve', resolve_side_effect):
            result = autoreload.iter_modules_and_files((), frozenset(['good.py', 'bad.py']))
        self.assertIn(temp, result)

    def test_iter_modules_and_files_logs_debug_on_value_error(self):
        with mock.patch.object(Path, 'resolve', side_effect=ValueError('logging test')):
            with mock.patch.object(autoreload.logger, 'debug') as mocked_debug:
                result = autoreload.iter_modules_and_files((), frozenset(['x.py']))
        self.assertEqual(result, frozenset())
        self.assertTrue(mocked_debug.called)
        called_args = mocked_debug.call_args[0][0] if mocked_debug.call_args else ''
        self.assertIn('raised when resolving path', called_args)

from unittest import mock
import tempfile
import sys
from pathlib import Path
from unittest import mock
from django.test import SimpleTestCase
from django.utils import autoreload
from pathlib import Path
import tempfile
import sys
import os

class ValueErrorPathResolveTests(SimpleTestCase):

    def setUp(self):
        self._tempdir = tempfile.TemporaryDirectory()
        self.valid_dir = Path(self._tempdir.name).resolve().absolute()
        self.valid_file = self.valid_dir / 'real.py'
        self.valid_file.touch()
        try:
            autoreload.iter_modules_and_files.cache_clear()
        except Exception:
            pass

    def tearDown(self):
        self._tempdir.cleanup()

class SysPathDirectoriesValueErrorTests(SimpleTestCase):

    def setUp(self):
        self._tempdir = tempfile.TemporaryDirectory()
        self.valid_dir = Path(self._tempdir.name).resolve().absolute()
        self.valid_file = self.valid_dir / 'file.txt'
        self.valid_file.touch()

    def tearDown(self):
        self._tempdir.cleanup()

import sys
from pathlib import Path
import types
import tempfile
from unittest import mock
import sys
import tempfile
import os
import types
from pathlib import Path
from unittest import mock
from django.test import SimpleTestCase
from django.test.utils import extend_sys_path
from django.utils import autoreload

class ValueErrorPathHandlingTests(SimpleTestCase):

    def setUp(self):
        autoreload.iter_modules_and_files.cache_clear()

    def tearDown(self):
        autoreload.iter_modules_and_files.cache_clear()

from unittest import mock
from pathlib import Path
import sys
from django.utils import autoreload
from django.utils.autoreload import iter_modules_and_files, sys_path_directories
from unittest import mock
from django.test import SimpleTestCase
from pathlib import Path
import sys
from django.utils import autoreload
from django.utils.autoreload import iter_modules_and_files, sys_path_directories

class ValueErrorHandlingTests(SimpleTestCase):

    def setUp(self):
        try:
            iter_modules_and_files.cache_clear()
        except AttributeError:
            pass

    def test_iter_modules_and_files_ignores_valueerror_unexpected_message(self):
        self._assert_iter_modules_and_files_ignores_valueerror('unexpected error')

    def test_iter_modules_and_files_ignores_valueerror_empty_message(self):
        self._assert_iter_modules_and_files_ignores_valueerror('')

    def test_iter_modules_and_files_ignores_valueerror_whitespace_message(self):
        self._assert_iter_modules_and_files_ignores_valueerror(' ')

    def test_iter_modules_and_files_ignores_valueerror_numeric_message(self):
        self._assert_iter_modules_and_files_ignores_valueerror('0')

    def test_iter_modules_and_files_ignores_valueerror_long_message(self):
        self._assert_iter_modules_and_files_ignores_valueerror('some long path error description')

from pathlib import Path
from unittest import mock
from pathlib import Path
import tempfile
import shutil
import os
from unittest import mock
from django.test import SimpleTestCase
from django.utils import autoreload
_orig_resolve = Path.resolve

class IterModulesAndFilesValueErrorTests(SimpleTestCase):

    def setUp(self):
        try:
            autoreload.iter_modules_and_files.cache_clear()
        except AttributeError:
            pass
        self.tmpdir = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.tmpdir)
        self.valid_file = Path(self.tmpdir) / 'valid.py'
        self.valid_file.parent.mkdir(parents=True, exist_ok=True)
        self.valid_file.write_text('# test')

    def tearDown(self):
        try:
            autoreload.iter_modules_and_files.cache_clear()
        except AttributeError:
            pass

import sys
import tempfile
import shutil
import types
from types import SimpleNamespace
from pathlib import Path
from unittest import mock
import sys
import tempfile
import shutil
import types
from types import SimpleNamespace
from pathlib import Path
from unittest import mock
from django.test import SimpleTestCase
from django.utils import autoreload

class ValueErrorHandlingTests(SimpleTestCase):

    def setUp(self):
        self._tmpdir = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self._tmpdir)
        self.tmpdir = Path(self._tmpdir).resolve().absolute()
        self.good_file = self.tmpdir / 'good.py'
        self.good_file.parent.mkdir(exist_ok=True, parents=True)
        self.good_file.touch()
        autoreload.iter_modules_and_files.cache_clear()

    def test_iter_modules_and_files_ignores_valueerror_from_extra_file(self):
        bad = str(self.tmpdir / 'bad_extra.py')
        with self._patch_resolve_to_raise([bad], message='boom'):
            result = autoreload.iter_modules_and_files((), frozenset([bad]))
        self.assertEqual(result, frozenset())

    def test_iter_modules_and_files_includes_good_and_ignores_bad_extra_file(self):
        bad = str(self.tmpdir / 'bad_extra2.py')
        with self._patch_resolve_to_raise([bad], message='boom'):
            result = autoreload.iter_modules_and_files((), frozenset([bad, str(self.good_file)]))
        self.assertIn(self.good_file.resolve(), result)
        self.assertNotIn(Path(bad), result)

    def test_iter_modules_and_files_ignores_valueerror_from_module_origin(self):
        bad = str(self.tmpdir / 'bad_origin.py')
        mod = types.ModuleType('test_bad_origin')
        mod.__spec__ = SimpleNamespace(has_location=True, origin=bad, loader=SimpleNamespace())
        with self._patch_resolve_to_raise([bad], message='boom'):
            result = autoreload.iter_modules_and_files((mod,), frozenset())
        self.assertEqual(result, frozenset())

    def test_iter_modules_and_files_with_module_and_extra_file_combination(self):
        bad = str(self.tmpdir / 'bad_combo.py')
        mod = types.ModuleType('test_bad_combo')
        mod.__spec__ = SimpleNamespace(has_location=True, origin=bad, loader=SimpleNamespace())
        with self._patch_resolve_to_raise([bad], message='boom'):
            result = autoreload.iter_modules_and_files((mod,), frozenset([str(self.good_file)]))
        self.assertIn(self.good_file.resolve(), result)
        self.assertNotIn(Path(bad), result)

    def test_iter_modules_and_files_ignores_valueerror_for_main_module_file(self):
        bad = str(self.tmpdir / 'bad_main.py')
        main_mod = types.ModuleType('__main__')
        main_mod.__file__ = bad
        with self._patch_resolve_to_raise([bad], message='boom'):
            result = autoreload.iter_modules_and_files((main_mod,), frozenset())
        self.assertEqual(result, frozenset())

from unittest import mock
import tempfile
from pathlib import Path
import types
from unittest import mock
import tempfile
from pathlib import Path
import types
from django.test import SimpleTestCase
from django.utils import autoreload

class TestIterModulesValueErrorHandling(SimpleTestCase):

    def setUp(self):
        autoreload.iter_modules_and_files.cache_clear()

    def test_iter_modules_and_files_swallow_generic_valueerror_from_extra_files(self):
        with self._patch_resolve_raising('some other error'):
            result = autoreload.iter_modules_and_files((), frozenset(['/nonexistent/path']))
        self.assertEqual(result, frozenset())

    def test_iter_modules_and_files_swallow_empty_valueerror_message(self):
        with self._patch_resolve_raising(''):
            result = autoreload.iter_modules_and_files((), frozenset(['/another/bad/path']))
        self.assertEqual(result, frozenset())

    def test_iter_modules_and_files_swallow_unicode_valueerror_message(self):
        with self._patch_resolve_raising('ユニコードエラー'):
            result = autoreload.iter_modules_and_files((), frozenset(['/unicode/bad']))
        self.assertEqual(result, frozenset())

    def test_iter_modules_and_files_swallow_null_phrase_message(self):
        with self._patch_resolve_raising('Null byte in path'):
            result = autoreload.iter_modules_and_files((), frozenset(['/nullbyte/bad']))
        self.assertEqual(result, frozenset())

    def test_iter_modules_and_files_handles_valueerror_from_main_module_file(self):
        main_mod = types.ModuleType('__main__')
        main_mod.__file__ = '/fake/main/file.py'
        if hasattr(main_mod, '__spec__'):
            del main_mod.__spec__
        with self._patch_resolve_raising('main module path error'):
            result = autoreload.iter_modules_and_files((main_mod,), frozenset())
        self.assertEqual(result, frozenset())

    def test_iter_modules_and_files_handles_valueerror_from_spec_origin(self):
        spec = types.SimpleNamespace(has_location=True, loader=object(), origin='/spec/origin.py')
        mod = types.ModuleType('test_spec_module')
        mod.__spec__ = spec
        with self._patch_resolve_raising('spec origin problem'):
            result = autoreload.iter_modules_and_files((mod,), frozenset())
        self.assertEqual(result, frozenset())

    def test_iter_modules_and_files_swallow_various_valueerror_messages_repeated(self):
        messages = ['msg1', 'embedded null byte', 'another msg', '']
        for msg in messages:
            autoreload.iter_modules_and_files.cache_clear()
            with self.subTest(msg=msg):
                with self._patch_resolve_raising(msg):
                    result = autoreload.iter_modules_and_files((), frozenset(['/bad/%s' % msg]))
                self.assertEqual(result, frozenset())

from unittest import mock
from django.test import SimpleTestCase
from pathlib import Path
import tempfile
import shutil
import os
import sys
import types
from django.utils import autoreload
from unittest import mock
from django.test import SimpleTestCase
from pathlib import Path
import tempfile
import shutil
import os
import sys
import types
from django.utils import autoreload

class ValueErrorHandlingTests(SimpleTestCase):

    def setUp(self):
        self._td = tempfile.TemporaryDirectory()
        self.addCleanup(self._td.cleanup)
        self.tempdir = Path(self._td.name).resolve().absolute()
        self.good_file = self.tempdir / 'good.py'
        self.good_file.parent.mkdir(parents=True, exist_ok=True)
        self.good_file.touch()
        autoreload.iter_modules_and_files.cache_clear()