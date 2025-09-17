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