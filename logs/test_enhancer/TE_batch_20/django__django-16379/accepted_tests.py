def test_has_key_race_os_path_exists_true_open_raises(self):
    key = 'race_file_1'
    fname = cache._key_to_file(key)
    with mock.patch('os.path.exists', return_value=True), mock.patch('builtins.open', side_effect=FileNotFoundError) as mocked_open:
        self.assertIs(cache.has_key(key), False)
        mocked_open.assert_called_once_with(fname, 'rb')

def test_has_key_race_with_version_argument(self):
    key = 'race_file_versioned'
    version = 2
    fname = cache._key_to_file(key, version=version)
    with mock.patch('os.path.exists', return_value=True), mock.patch('builtins.open', side_effect=FileNotFoundError) as mocked_open:
        self.assertIs(cache.has_key(key, version=version), False)
        mocked_open.assert_called_once_with(fname, 'rb')

def test_in_operator_uses_has_key_and_handles_race(self):
    key = 'race_in_operator'
    fname = cache._key_to_file(key)
    with mock.patch('os.path.exists', return_value=True), mock.patch('builtins.open', side_effect=FileNotFoundError) as mocked_open:
        self.assertNotIn(key, cache)
        mocked_open.assert_called_once_with(fname, 'rb')

def test_has_key_race_for_prefixed_cache(self):
    prefixed_cache = caches['prefix']
    key = 'race_prefixed'
    fname = prefixed_cache._key_to_file(key)
    with mock.patch('os.path.exists', return_value=True), mock.patch('builtins.open', side_effect=FileNotFoundError) as mocked_open:
        self.assertIs(prefixed_cache.has_key(key), False)
        mocked_open.assert_called_once_with(fname, 'rb')

def test_has_key_race_for_v2_cache_default_version(self):
    v2_cache = caches['v2']
    key = 'race_v2'
    fname = v2_cache._key_to_file(key)
    with mock.patch('os.path.exists', return_value=True), mock.patch('builtins.open', side_effect=FileNotFoundError) as mocked_open:
        self.assertIs(v2_cache.has_key(key), False)
        mocked_open.assert_called_once_with(fname, 'rb')

def test_has_key_called_once_when_open_raises_FileNotFoundError(self):
    key = 'race_called_once'
    fname = cache._key_to_file(key)
    with mock.patch('builtins.open', side_effect=FileNotFoundError) as mocked_open:
        self.assertIs(cache.has_key(key), False)
        mocked_open.assert_called_once_with(fname, 'rb')

def test_has_key_race_handles_unicode_key(self):
    key = '键-with-unicode-清'
    fname = cache._key_to_file(key)
    with mock.patch('os.path.exists', return_value=True), mock.patch('builtins.open', side_effect=FileNotFoundError) as mocked_open:
        self.assertIs(cache.has_key(key), False)
        mocked_open.assert_called_once_with(fname, 'rb')

def test_has_key_with_version_and_prefix_combination_race(self):
    prefixed_cache = caches['prefix']
    key = 'race_prefixed_version'
    version = 3
    fname = prefixed_cache._key_to_file(key, version=version)
    with mock.patch('os.path.exists', return_value=True), mock.patch('builtins.open', side_effect=FileNotFoundError) as mocked_open:
        self.assertIs(prefixed_cache.has_key(key, version=version), False)
        mocked_open.assert_called_once_with(fname, 'rb')

def test_has_key_does_not_propagate_FileNotFoundError_on_pathlib_location(self):
    key = 'race_pathlib'
    fname = cache._key_to_file(key)
    with mock.patch('os.path.exists', return_value=True), mock.patch('builtins.open', side_effect=FileNotFoundError) as mocked_open:
        self.assertIs(cache.has_key(key), False)
        mocked_open.assert_called_once_with(fname, 'rb')

def test_has_key_in_operator_with_prefixed_cache_handles_race(self):
    prefixed_cache = caches['prefix']
    key = 'race_in_prefixed'
    fname = prefixed_cache._key_to_file(key)
    with mock.patch('os.path.exists', return_value=True), mock.patch('builtins.open', side_effect=FileNotFoundError) as mocked_open:
        self.assertNotIn(key, prefixed_cache)
        mocked_open.assert_called_once_with(fname, 'rb')

def test_has_key_race_handling_versioned(self):
    self.assertIs(cache.add('race_versioned', 'value', version=2), True)
    with mock.patch('builtins.open', side_effect=FileNotFoundError) as mocked_open:
        self.assertIs(cache.has_key('race_versioned', version=2), False)
        mocked_open.assert_called_once()

def test_in_operator_race_handling_for_filebased(self):
    self.assertIs(cache.add('race_in', 'value'), True)
    with mock.patch('builtins.open', side_effect=FileNotFoundError):
        self.assertNotIn('race_in', cache)

def test_prefix_cache_has_key_race_handling(self):
    self.assertIs(caches['prefix'].add('race_prefix', 'value'), True)
    with mock.patch('builtins.open', side_effect=FileNotFoundError):
        self.assertIs(caches['prefix'].has_key('race_prefix'), False)

def test_v2_cache_has_key_race_handling(self):
    self.assertIs(caches['v2'].add('race_v2', 'value'), True)
    with mock.patch('builtins.open', side_effect=FileNotFoundError):
        self.assertIs(caches['v2'].has_key('race_v2'), False)

def test_has_key_propagates_os_error(self):
    self.assertIs(cache.add('race_oserror', 'value'), True)
    with mock.patch('builtins.open', side_effect=OSError):
        with self.assertRaises(OSError):
            cache.has_key('race_oserror')

def test_has_key_called_with_correct_filename(self):
    key = 'race_check_name'
    self.assertIs(cache.add(key, 'value'), True)
    fname = cache._key_to_file(key)
    with mock.patch('builtins.open', side_effect=FileNotFoundError) as mocked_open:
        self.assertIs(cache.has_key(key), False)
        mocked_open.assert_called_once_with(fname, 'rb')

def test_has_key_race_handling_multiple_calls(self):
    self.assertIs(cache.add('race_multi_1', 'value1'), True)
    self.assertIs(cache.add('race_multi_2', 'value2'), True)
    with mock.patch('builtins.open', side_effect=FileNotFoundError) as mocked_open:
        self.assertIs(cache.has_key('race_multi_1'), False)
        self.assertIs(cache.has_key('race_multi_2'), False)
        self.assertEqual(mocked_open.call_count, 2)

def test_has_key_unicode_key_race_handling(self):
    key = 'ключ-раcсин'
    self.assertIs(cache.add(key, 'value'), True)
    with mock.patch('builtins.open', side_effect=FileNotFoundError):
        self.assertIs(cache.has_key(key), False)

def test_has_key_does_not_swallow_other_exceptions(self):
    self.assertIs(cache.add('race_other_exc', 'value'), True)

    class CustomError(Exception):
        pass
    with mock.patch('builtins.open', side_effect=CustomError):
        with self.assertRaises(CustomError):
            cache.has_key('race_other_exc')

from unittest import mock
import os
import time
from django.core.cache import cache, caches
from django.test import override_settings

def test_has_key_handles_open_enoent_race(self):
    self.assertIs(cache.add('race-key', 'value'), True)
    with mock.patch('builtins.open', side_effect=FileNotFoundError) as mocked_open:
        self.assertIs(cache.has_key('race-key'), False)
        mocked_open.assert_called_once()

def test_has_key_handles_open_enoent_race_with_version(self):
    self.assertIs(cache.add('race-key-v', 'value', version=2), True)
    with mock.patch('builtins.open', side_effect=FileNotFoundError) as mocked_open:
        self.assertIs(cache.has_key('race-key-v', version=2), False)
        mocked_open.assert_called_once()

def test_has_key_propagates_other_exceptions(self):
    self.assertIs(cache.add('other-exc', 'value'), True)
    with mock.patch('builtins.open', side_effect=OSError('boom')):
        with self.assertRaises(OSError):
            cache.has_key('other-exc')

def test_has_key_propagates_permission_error(self):
    self.assertIs(cache.add('perm-exc', 'value'), True)
    with mock.patch('builtins.open', side_effect=PermissionError('nope')):
        with self.assertRaises(PermissionError):
            cache.has_key('perm-exc')

def test_has_key_empty_file_considered_expired_and_removed(self):
    fname = cache._key_to_file('empty-file-test')
    os.makedirs(os.path.dirname(fname), exist_ok=True)
    with open(fname, 'wb') as fh:
        fh.write(b'')
    self.assertIs(cache.has_key('empty-file-test'), False)
    self.assertFalse(os.path.exists(fname))

def test_has_key_no_file_returns_false(self):
    cache.delete('definitely-not-there')
    self.assertIs(cache.has_key('definitely-not-there'), False)

def test_has_key_true_when_not_expired(self):
    cache.set('fresh-key', 'v', timeout=10)
    self.assertIs(cache.has_key('fresh-key'), True)

def test_has_key_false_when_expired(self):
    cache.set('short-lived', 'v', timeout=1)
    time.sleep(1.1)
    self.assertIs(cache.has_key('short-lived'), False)

def test_has_key_with_versioning(self):
    cache.set('vers-key', 'v1', version=1)
    cache.set('vers-key', 'v2', version=2)
    self.assertIs(cache.has_key('vers-key', version=1), True)
    self.assertIs(cache.has_key('vers-key', version=2), True)
    self.assertIs(cache.has_key('vers-key', version=3), False)

def test_has_key_open_called_once_on_race(self):
    self.assertIs(cache.add('race-once', 'value'), True)
    with mock.patch('builtins.open', side_effect=FileNotFoundError) as mocked_open:
        self.assertIs(cache.has_key('race-once'), False)
        mocked_open.assert_called_once()

from unittest import mock
import os
import pickle
import zlib
import shutil
import tempfile
import time
from django.conf import settings
from django.core.cache import cache
from django.test import TestCase, override_settings
from django.test.signals import setting_changed

@override_settings(CACHES={'default': {'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache'}})
class AdditionalFileBasedCacheRegressionTests(TestCase):
    """
    Additional regression tests for the file-based cache backend focusing on
    has_key() race handling and expiration behavior.
    """

    def setUp(self):
        self.dirname = tempfile.mkdtemp()
        for cache_params in settings.CACHES.values():
            cache_params['LOCATION'] = self.dirname
        setting_changed.send(self.__class__, setting='CACHES', enter=False)

import os
import shutil
import tempfile
import time
import pickle
import zlib
import unittest
from unittest import mock
from django.core.cache.backends.filebased import FileBasedCache

class FileBasedCacheRegressionTests(unittest.TestCase):

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        self.cache = FileBasedCache(self.tmpdir, params={})

    def tearDown(self):
        try:
            shutil.rmtree(self.tmpdir)
        except FileNotFoundError:
            pass

from unittest import mock
import os
import tempfile
import time
import stat
import shutil
import sys
from pathlib import Path
from django.conf import settings
from django.test import TestCase, override_settings
from django.test.signals import setting_changed
from django.core.cache import caches, cache
from django.core.cache.backends.filebased import FileBasedCache

@override_settings(CACHES={'default': {'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache'}})
class AdditionalFileBasedCacheTests(TestCase):

    def setUp(self):
        super().setUp()
        self.dirname = tempfile.mkdtemp()
        for cache_params in settings.CACHES.values():
            cache_params['LOCATION'] = self.dirname
        setting_changed.send(self.__class__, setting='CACHES', enter=False)
        self.cache = caches['default']

    def tearDown(self):
        super().tearDown()
        shutil.rmtree(self.dirname, ignore_errors=True)

import zlib

def test_has_key_open_raises_filenotfound(self):
    cache.set('race1', 'value')
    with mock.patch('builtins.open', side_effect=FileNotFoundError()) as mocked_open:
        self.assertIs(cache.has_key('race1'), False)
        mocked_open.assert_called_once()

def test_has_key_open_raises_oserror_propagates(self):
    with mock.patch('builtins.open', side_effect=OSError('boom')):
        with self.assertRaises(OSError):
            cache.has_key('does_not_matter')

def test_has_key_with_version_handles_filenotfound(self):
    cache.set('race_version', 'value', version=2)
    with mock.patch('builtins.open', side_effect=FileNotFoundError()) as mocked_open:
        self.assertIs(cache.has_key('race_version', version=2), False)
        mocked_open.assert_called_once()

def test_has_key_expired_file_deleted(self):
    key = 'expired_key'
    cache.set(key, 'value', timeout=60)
    fname = cache._key_to_file(key)
    expiry = time.time() - 10.0
    with open(fname, 'wb') as fh:
        fh.write(pickle.dumps(expiry))
        fh.write(zlib.compress(pickle.dumps('stale')))
    self.assertTrue(os.path.exists(fname))
    self.assertIs(cache.has_key(key), False)
    self.assertFalse(os.path.exists(fname))

def test_has_key_missing_file_returns_false(self):
    key = 'no_such_key'
    fname = cache._key_to_file(key)
    if os.path.exists(fname):
        os.remove(fname)
    self.assertIs(cache.has_key(key), False)

def test_has_key_does_not_create_file(self):
    key = 'no_create_key'
    before = set(os.listdir(self.dirname))
    cache.has_key(key)
    after = set(os.listdir(self.dirname))
    self.assertEqual(before, after)

def test_has_key_unexpired_true(self):
    key = 'live_key'
    cache.set(key, 'ok', timeout=10)
    self.assertIs(cache.has_key(key), True)

def test_has_key_is_expired_raising_filenotfound_is_handled(self):
    key = 'concurrent_delete'
    cache.set(key, 'v', timeout=10)
    with mock.patch.object(cache.__class__, '_is_expired', side_effect=FileNotFoundError()):
        self.assertIs(cache.has_key(key), False)

def test_has_key_is_expired_raising_other_errors_propagates(self):
    key = 'concurrent_other'
    cache.set(key, 'v', timeout=10)
    with mock.patch.object(cache.__class__, '_is_expired', side_effect=OSError('boom')):
        with self.assertRaises(OSError):
            cache.has_key(key)

def test_has_key_uses_expected_filename_when_opening(self):
    key = 'check_fname'
    expected = cache._key_to_file(key)
    m = mock.mock_open(read_data=b'')
    with mock.patch('builtins.open', m) as mocked_open:
        cache.has_key(key)
        mocked_open.assert_called_with(expected, 'rb')

import errno
import os
import pickle
import shutil
import tempfile
from unittest import mock
from django.test import SimpleTestCase
from django.core.cache.backends.filebased import FileBasedCache
from django.core.cache.backends.base import DEFAULT_TIMEOUT

class FileBasedCacheHasKeyRegressionTests(SimpleTestCase):

    def setUp(self):
        self.dirname = tempfile.mkdtemp()
        self.cache = FileBasedCache(self.dirname, params={})

    def tearDown(self):
        try:
            shutil.rmtree(self.dirname)
        except OSError:
            pass

from django.test import TestCase, override_settings
from django.test.signals import setting_changed
from django.conf import settings
from django.core.cache import cache, caches
import tempfile
import shutil
import os
import time
from unittest import mock

@override_settings(CACHES={'default': {'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache'}})
class FileBasedCacheRegressionTests(TestCase):
    """
    Regression tests for FileBasedCache.has_key race conditions and error
    handling. These tests mirror real-world races where files may be removed
    between existence checks and open(), and ensure only FileNotFoundError
    is swallowed into a False return value.
    """

    def setUp(self):
        super().setUp()
        self.dirname = tempfile.mkdtemp()
        for cache_params in settings.CACHES.values():
            cache_params['LOCATION'] = self.dirname
        setting_changed.send(self.__class__, setting='CACHES', enter=False)

    def tearDown(self):
        super().tearDown()
        try:
            shutil.rmtree(self.dirname)
        except FileNotFoundError:
            pass

import os
import shutil
import tempfile
from unittest import mock
from django.conf import settings
from django.test import override_settings, TestCase
from django.test.signals import setting_changed
from django.core.cache import cache, caches

@override_settings(CACHES={'default': {'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache'}})
class FileBasedHasKeyRaceTests(TestCase):

    def setUp(self):
        super().setUp()
        self.dirname = tempfile.mkdtemp()
        for cache_params in settings.CACHES.values():
            cache_params['LOCATION'] = self.dirname
        setting_changed.send(self.__class__, setting='CACHES', enter=False)

import tempfile
import shutil
import os
from unittest import mock
from django.test import TestCase
from django.core.cache.backends.filebased import FileBasedCache

class FileBasedCacheHasKeyRaceTests(TestCase):

    def setUp(self):
        self.dirname = tempfile.mkdtemp()
        self.cache = FileBasedCache(self.dirname, {})