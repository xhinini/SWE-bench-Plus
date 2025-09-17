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