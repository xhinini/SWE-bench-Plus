from django.test import SimpleTestCase
from django.views.debug import SafeExceptionReporterFilter
from django.conf import settings

class RegressionCleanseListTupleTests(SimpleTestCase):

    def test_cleanse_setting_with_list_subclass_direct(self):
        initial = [{'login': 'cooper', 'password': 'secret'}]

        class BadList(list):

            def __init__(self):
                super().__init__()
        bad = BadList.__new__(BadList)
        list.__init__(bad, initial)
        reporter_filter = SafeExceptionReporterFilter()
        result = reporter_filter.cleanse_setting('FOOBAR', bad)
        self.assertIsInstance(result, list)
        self.assertEqual(result[0]['password'], reporter_filter.cleansed_substitute)

    def test_cleanse_setting_with_list_subclass_via_get_safe_settings(self):
        initial = [{'login': 'cooper', 'password': 'secret'}]

        class BadList(list):

            def __init__(self):
                super().__init__()
        bad = BadList.__new__(BadList)
        list.__init__(bad, initial)
        reporter_filter = SafeExceptionReporterFilter()
        with self.settings(BADLIST=bad):
            safe = reporter_filter.get_safe_settings()
        self.assertIn('BADLIST', safe)
        self.assertIsInstance(safe['BADLIST'], list)
        self.assertEqual(safe['BADLIST'][0]['password'], reporter_filter.cleansed_substitute)

    def test_cleanse_setting_with_tuple_subclass_direct(self):
        initial = ({'SECRET_KEY': 's'},)

        class BadTuple(tuple):

            def __new__(cls, *args, **kwargs):
                raise TypeError('Bad tuple constructor')
        bad = tuple.__new__(BadTuple, initial)
        reporter_filter = SafeExceptionReporterFilter()
        result = reporter_filter.cleanse_setting('FOOBAR', bad)
        self.assertIsInstance(result, tuple)
        self.assertEqual(result[0]['SECRET_KEY'], reporter_filter.cleansed_substitute)

    def test_cleanse_setting_with_tuple_subclass_via_get_safe_settings(self):
        initial = ({'SECRET_KEY': 's'},)

        class BadTuple(tuple):

            def __new__(cls, *args, **kwargs):
                raise TypeError('Bad tuple constructor')
        bad = tuple.__new__(BadTuple, initial)
        reporter_filter = SafeExceptionReporterFilter()
        with self.settings(BADTUP=bad):
            safe = reporter_filter.get_safe_settings()
        self.assertIn('BADTUP', safe)
        self.assertIsInstance(safe['BADTUP'], tuple)
        self.assertEqual(safe['BADTUP'][0]['SECRET_KEY'], reporter_filter.cleansed_substitute)

from django.test import SimpleTestCase
from django.views.debug import SafeExceptionReporterFilter, CallableSettingWrapper
from django.utils.regex_helper import _lazy_re_compile
import types

class ListTupleCleanseTests(SimpleTestCase):

    def setUp(self):
        self.filter = SafeExceptionReporterFilter()

from django.test import SimpleTestCase
from django.views.debug import SafeExceptionReporterFilter, CallableSettingWrapper

class SafeExceptionReporterFilterRegressionTests(SimpleTestCase):

    def setUp(self):
        self.filter = SafeExceptionReporterFilter()

from django.views.debug import SafeExceptionReporterFilter, CallableSettingWrapper
from django.test import SimpleTestCase
from django.views.debug import SafeExceptionReporterFilter, CallableSettingWrapper

class BadListTests(SimpleTestCase):

    def setUp(self):
        self.filter = SafeExceptionReporterFilter()

    def test_custom_list_subclass_with_sensitive_inner_dict_is_cleansed(self):
        secret = 'very_secret_value'
        bad = self._make_bad_list([{'PASSWORD': secret}])
        cleansed = self.filter.cleanse_setting('SETTING_NAME', bad)
        self.assertNotIn(secret, repr(cleansed))
        self.assertIn(self.filter.cleansed_substitute, repr(cleansed))

    def test_custom_list_subclass_wraps_callable_element(self):
        called = {'flag': False}

        def callable_setting():
            called['flag'] = True
            return 'I ran'
        bad = self._make_bad_list([callable_setting])
        cleansed = self.filter.cleanse_setting('SETTING_NAME', bad)
        self.assertFalse(called['flag'], 'Callable was unexpectedly executed')
        found_wrapper = False
        for item in list(cleansed) if hasattr(cleansed, '__iter__') else [cleansed]:
            if isinstance(item, CallableSettingWrapper):
                found_wrapper = True
                break
        self.assertTrue(found_wrapper, 'CallableSettingWrapper not present in cleansed output')

    def test_custom_list_subclass_cleanses_nested_dicts(self):
        secret = 'nested_secret'
        bad = self._make_bad_list([{'outer': {'PASSWORD': secret}}])
        cleansed = self.filter.cleanse_setting('SETTING_NAME', bad)
        self.assertNotIn(secret, repr(cleansed))
        self.assertIn(self.filter.cleansed_substitute, repr(cleansed))

    def test_custom_list_subclass_cleanses_inner_tuple_contents(self):
        secret = 'tuple_secret'
        bad = self._make_bad_list([({'SECRET_KEY': secret},)])
        cleansed = self.filter.cleanse_setting('SETTING_NAME', bad)
        self.assertNotIn(secret, repr(cleansed))
        self.assertIn(self.filter.cleansed_substitute, repr(cleansed))

    def test_custom_list_subclass_with_multiple_sensitive_entries(self):
        secret1 = 's1'
        secret2 = 's2'
        bad = self._make_bad_list([{'API_KEY': secret1}, {'PASSWORD': secret2}])
        cleansed = self.filter.cleanse_setting('SETTING_NAME', bad)
        self.assertNotIn(secret1, repr(cleansed))
        self.assertNotIn(secret2, repr(cleansed))
        self.assertEqual(repr(cleansed).count(self.filter.cleansed_substitute), 2)

    def test_custom_list_subclass_cleanses_deeply_nested_structures(self):
        secret = 'deep_secret'
        deep = [{'level1': [{'level2': {'PASSWORD': secret}}]}]
        bad = self._make_bad_list(deep)
        cleansed = self.filter.cleanse_setting('SETTING_NAME', bad)
        self.assertNotIn(secret, repr(cleansed))
        self.assertIn(self.filter.cleansed_substitute, repr(cleansed))

    def test_custom_list_subclass_preserves_inner_tuple_types(self):
        secret = 'tuple_inner_secret'
        bad = self._make_bad_list([({'PASSWORD': secret},)])
        cleansed = self.filter.cleanse_setting('SETTING_NAME', bad)
        found_tuple = False
        for item in list(cleansed):
            if isinstance(item, tuple):
                found_tuple = True
                self.assertNotIn(secret, repr(item))
                self.assertIn(self.filter.cleansed_substitute, repr(item))
        self.assertTrue(found_tuple, 'No tuple found in cleansed result')

    def test_custom_list_subclass_recurses_in_list_of_lists(self):
        secret = 'll_secret'
        bad = self._make_bad_list([[{'PASSWORD': secret}]])
        cleansed = self.filter.cleanse_setting('SETTING_NAME', bad)
        self.assertNotIn(secret, repr(cleansed))
        self.assertIn(self.filter.cleansed_substitute, repr(cleansed))