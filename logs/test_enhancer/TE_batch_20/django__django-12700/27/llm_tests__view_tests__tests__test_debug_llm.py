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

from django.test import SimpleTestCase
from django.views.debug import SafeExceptionReporterFilter, CallableSettingWrapper

class CleanseSettingNonStringKeyTests(SimpleTestCase):

    def setUp(self):
        self.filter = SafeExceptionReporterFilter()
        self.sub = self.filter.cleansed_substitute

from django.views.debug import SafeExceptionReporterFilter, CallableSettingWrapper
from django.test import SimpleTestCase, override_settings
from django.utils.datastructures import MultiValueDict
from django.views.debug import SafeExceptionReporterFilter, CallableSettingWrapper

class ListTupleCleansingTests(SimpleTestCase):

    def setUp(self):
        self.filter = SafeExceptionReporterFilter()
        self.sub = self.filter.cleansed_substitute

from collections import namedtuple
from collections import namedtuple
from django.test import SimpleTestCase, override_settings
from django.views.debug import SafeExceptionReporterFilter

class RegressionSafeExceptionReporterFilterTests(SimpleTestCase):
    def setUp(self):
        self.filter = SafeExceptionReporterFilter()
        self.cleansed = self.filter.cleansed_substitute

    def test_namedtuple_direct_cleansed(self):
        # A namedtuple (tuple subclass) containing a dict with a sensitive key
        NT = namedtuple('NT', 'a b')
        val = NT('plain', {'API_KEY': 'secret-value'})
        cleaned = self.filter.cleanse_setting('SETTING_NAME', val)
        # Expect the API_KEY inside the tuple to be cleansed
        self.assertEqual(cleaned[1]['API_KEY'], self.cleansed)

    def test_namedtuple_inside_tuple_cleansed(self):
        NT = namedtuple('NT', 'a b')
        inner = NT('x', {'TOKEN': 'tokensecret'})
        tup = (inner,)
        cleaned = self.filter.cleanse_setting('SETTING_NAME', tup)
        self.assertEqual(cleaned[0][1]['TOKEN'], self.cleansed)

    def test_namedtuple_inside_list_cleansed(self):
        NT = namedtuple('NT', 'a b')
        inner = NT('x', {'SECRET_KEY': 'verysecret'})
        lst = [inner]
        cleaned = self.filter.cleanse_setting('SETTING_NAME', lst)
        self.assertEqual(cleaned[0][1]['SECRET_KEY'], self.cleansed)

    def test_namedtuple_nested_in_dict_value_cleansed(self):
        NT = namedtuple('NT', 'a b')
        inner = NT('left', {'API_KEY': 'innersecret'})
        data = {'nested': inner}
        cleaned = self.filter.cleanse_setting('SETTING_NAME', data)
        self.assertEqual(cleaned['nested'][1]['API_KEY'], self.cleansed)

    def test_tuple_subclass_with_strange_constructor_cleansed(self):
        # A custom tuple subclass with a constructor signature that will
        # raise TypeError if called with a single iterable.
        class WeirdTuple(tuple):
            def __new__(cls, a, b):
                # expects two positional args; calling WeirdTuple(iterable) will fail
                return super().__new__(cls, (a, b))
        wt = WeirdTuple('keep', {'API_KEY': 'weirdsecret'})
        cleaned = self.filter.cleanse_setting('SETTING_NAME', wt)
        # Ensure inner dict has been cleansed despite WeirdTuple constructor
        self.assertEqual(cleaned[1]['API_KEY'], self.cleansed)

    def test_list_of_namedtuples_cleansed(self):
        NT = namedtuple('NT', 'a b')
        items = [NT('alpha', {'TOKEN': 't1'}), NT('beta', {'TOKEN': 't2'})]
        cleaned = self.filter.cleanse_setting('SETTING_NAME', items)
        self.assertEqual(cleaned[0][1]['TOKEN'], self.cleansed)
        self.assertEqual(cleaned[1][1]['TOKEN'], self.cleansed)

    def test_tuple_of_namedtuples_cleansed(self):
        NT = namedtuple('NT', 'a b')
        items = (NT('one', {'API_KEY': 'a1'}), NT('two', {'API_KEY': 'a2'}))
        cleaned = self.filter.cleanse_setting('SETTING_NAME', items)
        self.assertEqual(cleaned[0][1]['API_KEY'], self.cleansed)
        self.assertEqual(cleaned[1][1]['API_KEY'], self.cleansed)

    def test_nested_structures_with_namedtuple_cleansed(self):
        NT = namedtuple('NT', 'a b')
        nested = {'group': [NT('n', {'SECRET_KEY': 'sval'}), ({'TOKEN': 'tok'},)]}
        cleaned = self.filter.cleanse_setting('SETTING_NAME', nested)
        # group is a list; its first element is a namedtuple whose dict should be cleansed
        self.assertEqual(cleaned['group'][0][1]['SECRET_KEY'], self.cleansed)
        # second element is a tuple containing a dict; ensure token is cleansed
        self.assertEqual(cleaned['group'][1][0]['TOKEN'], self.cleansed)

    @override_settings(MY_NT=None)
    def test_get_safe_settings_includes_cleansed_namedtuple(self):
        # Put a namedtuple into Django settings and ensure get_safe_settings
        # returns a cleansed representation.
        NT = namedtuple('NT', 'a b')
        nt_value = NT('p', {'API_KEY': 'supersecret'})
        with self.settings(DEBUG=False, MY_NT=nt_value):
            safe = self.filter.get_safe_settings()
            # The MY_NT setting should be present and have its inner dict cleansed
            self.assertIn('MY_NT', safe)
            self.assertEqual(safe['MY_NT'][1]['API_KEY'], self.cleansed)

    def test_mixed_namedtuple_and_plain_tuple_cleansed(self):
        NT = namedtuple('NT', 'a b')
        mixed = (NT('nt', {'TOKEN': 'tkn'}), ('plain', {'SECRET_KEY': 'sec'}))
        cleaned = self.filter.cleanse_setting('SETTING_NAME', mixed)
        self.assertEqual(cleaned[0][1]['TOKEN'], self.cleansed)
        self.assertEqual(cleaned[1][1]['SECRET_KEY'], self.cleansed)

from django.test import SimpleTestCase
from django.views.debug import SafeExceptionReporterFilter, CallableSettingWrapper

class SafeExceptionReporterFilterRegressionTests(SimpleTestCase):

    def test_cleanse_setting_with_list_subclass_returns_builtin_list(self):

        class BadList(list):

            def __init__(self, a, needed):
                super().__init__(a)
        bad = BadList([{'login': 'cooper', 'password': 'secret'}], object())
        reporter_filter = SafeExceptionReporterFilter()
        result = reporter_filter.cleanse_setting('SETTING_NAME', bad)
        self.assertIsInstance(result, list)
        self.assertNotIsInstance(result, BadList)
        self.assertEqual(result[0]['password'], reporter_filter.cleansed_substitute)

    def test_cleanse_setting_with_tuple_subclass_returns_builtin_tuple(self):

        class BadTuple(tuple):

            def __new__(cls, a, required):
                return super().__new__(cls, tuple(a))
        bad = BadTuple([{'SECRET_KEY': 's3cr3t'}], object())
        reporter_filter = SafeExceptionReporterFilter()
        result = reporter_filter.cleanse_setting('SETTING_NAME', bad)
        self.assertIsInstance(result, tuple)
        self.assertNotIsInstance(result, BadTuple)
        self.assertEqual(result[0]['SECRET_KEY'], reporter_filter.cleansed_substitute)

    def test_cleanse_setting_with_list_subclass_nested_in_dict(self):

        class BadList(list):

            def __init__(self, a, needed):
                super().__init__(a)
        bad = {'apps': BadList([{'name': 'app', 'api_key': 'abc'}], 1)}
        reporter_filter = SafeExceptionReporterFilter()
        result = reporter_filter.cleanse_setting('SETTING_NAME', bad)
        self.assertIsInstance(result['apps'], list)
        self.assertNotIsInstance(result['apps'], BadList)
        self.assertEqual(result['apps'][0]['api_key'], reporter_filter.cleansed_substitute)

    def test_cleanse_setting_with_tuple_subclass_nested_in_dict(self):

        class BadTuple(tuple):

            def __new__(cls, a, required):
                return super().__new__(cls, tuple(a))
        bad = {'items': BadTuple([{'TOKEN': 'tokval'}], 1)}
        reporter_filter = SafeExceptionReporterFilter()
        result = reporter_filter.cleanse_setting('SETTING_NAME', bad)
        self.assertIsInstance(result['items'], tuple)
        self.assertNotIsInstance(result['items'], BadTuple)
        self.assertEqual(result['items'][0]['TOKEN'], reporter_filter.cleansed_substitute)

    def test_cleanse_setting_with_list_subclass_nested_in_list(self):

        class BadList(list):

            def __init__(self, a, needed):
                super().__init__(a)
        bad = [BadList([{'login': 'cooper', 'password': 'secret'}], 1)]
        reporter_filter = SafeExceptionReporterFilter()
        result = reporter_filter.cleanse_setting('SETTING_NAME', bad)
        self.assertIsInstance(result, list)
        self.assertIsInstance(result[0], list)
        self.assertNotIsInstance(result[0], BadList)
        self.assertEqual(result[0][0]['password'], reporter_filter.cleansed_substitute)

    def test_cleanse_setting_with_tuple_subclass_nested_in_list(self):

        class BadTuple(tuple):

            def __new__(cls, a, required):
                return super().__new__(cls, tuple(a))
        bad = [BadTuple([{'API_KEY': 'value'}], 1)]
        reporter_filter = SafeExceptionReporterFilter()
        result = reporter_filter.cleanse_setting('SETTING_NAME', bad)
        self.assertIsInstance(result, list)
        self.assertIsInstance(result[0], tuple)
        self.assertNotIsInstance(result[0], BadTuple)
        self.assertEqual(result[0][0]['API_KEY'], reporter_filter.cleansed_substitute)

    def test_get_safe_settings_handles_list_subclass_setting(self):

        class BadList(list):

            def __init__(self, a, needed):
                super().__init__(a)
        bad = BadList([{'login': 'cooper', 'password': 'secret'}], 1)
        reporter_filter = SafeExceptionReporterFilter()
        result = reporter_filter.cleanse_setting('MY_SETTING', bad)
        self.assertIsInstance(result, list)
        self.assertEqual(result[0]['password'], reporter_filter.cleansed_substitute)

    def test_get_safe_settings_handles_tuple_subclass_setting(self):

        class BadTuple(tuple):

            def __new__(cls, a, required):
                return super().__new__(cls, tuple(a))
        bad = BadTuple([{'SECRET_KEY': 's3cr3t'}], 1)
        reporter_filter = SafeExceptionReporterFilter()
        result = reporter_filter.cleanse_setting('MY_SETTING', bad)
        self.assertIsInstance(result, tuple)
        self.assertEqual(result[0]['SECRET_KEY'], reporter_filter.cleansed_substitute)

    def test_callable_inside_list_subclass_is_wrapped_and_no_error(self):

        class BadList(list):

            def __init__(self, a, needed):
                super().__init__(a)

        def mycallable():
            return 'hi'
        bad = BadList([mycallable], 1)
        reporter_filter = SafeExceptionReporterFilter()
        result = reporter_filter.cleanse_setting('MY_SETTING', bad)
        self.assertIsInstance(result, list)
        self.assertTrue(isinstance(result[0], CallableSettingWrapper) or not callable(result[0]))

from django.test import SimpleTestCase
from django.views.debug import SafeExceptionReporterFilter

class SafeExceptionReporterFilterListTupleRegressionTests(SimpleTestCase):

    def setUp(self):
        self.filter = SafeExceptionReporterFilter()

import re
from django.test import override_settings, SimpleTestCase
from django.views.debug import SafeExceptionReporterFilter
from django.views.debug import CallableSettingWrapper
from django.conf import settings
from django.test import override_settings, SimpleTestCase
from django.views.debug import SafeExceptionReporterFilter, CallableSettingWrapper
import re

class CleanseListTupleEmptyKeyTests(SimpleTestCase):

    def test_list_recursion_uses_empty_key(self):
        """
        If the filter's hidden_settings matches an empty string, the
        recursive call for list elements should pass '' as the key, so
        that the hidden_settings test sees '' and will mask the element.
        The candidate patch passes the parent key instead of '', which
        causes a different result — this test detects that.
        """
        reporter = SafeExceptionReporterFilter()
        reporter.hidden_settings = re.compile('^$')
        value = [{'SECRET_KEY': 's'}, {'other': 'o'}]
        result = reporter.cleanse_setting('PARENT', value)
        expected = [reporter.cleansed_substitute, reporter.cleansed_substitute]
        self.assertEqual(result, expected)

    def test_tuple_recursion_uses_empty_key(self):
        """
        Same as test_list_recursion_uses_empty_key but for tuples.
        """
        reporter = SafeExceptionReporterFilter()
        reporter.hidden_settings = re.compile('^$')
        value = ({'SECRET_KEY': 's'}, {'other': 'o'})
        result = reporter.cleanse_setting('PARENT', value)
        expected = (reporter.cleansed_substitute, reporter.cleansed_substitute)
        self.assertEqual(result, expected)

    def test_nested_list_recursion_uses_empty_key(self):
        """
        Deeply nested lists should also be affected by the '' key when
        hidden_settings matches ''.
        """
        reporter = SafeExceptionReporterFilter()
        reporter.hidden_settings = re.compile('^$')
        value = [[{'SECRET_KEY': 's'}], [{'other': 'o'}]]
        result = reporter.cleanse_setting('PARENT', value)
        expected = [reporter.cleansed_substitute, reporter.cleansed_substitute]
        self.assertEqual(result, expected)

    def test_list_of_callables_with_empty_key_gets_masked(self):
        """
        If hidden_settings matches '', a list element that would otherwise
        be wrapped as CallableSettingWrapper should instead be masked by
        the empty-key match.
        """
        reporter = SafeExceptionReporterFilter()
        reporter.hidden_settings = re.compile('^$')

        def some_callable():
            return 'ok'
        value = [some_callable]
        result = reporter.cleanse_setting('PARENT', value)
        expected = [reporter.cleansed_substitute]
        self.assertEqual(result, expected)

    def test_tuple_of_callables_with_empty_key_gets_masked(self):
        """
        Same as test_list_of_callables_with_empty_key_gets_masked but for tuples.
        """
        reporter = SafeExceptionReporterFilter()
        reporter.hidden_settings = re.compile('^$')

        def some_callable():
            return 'ok'
        value = (some_callable,)
        result = reporter.cleanse_setting('PARENT', value)
        expected = (reporter.cleansed_substitute,)
        self.assertEqual(result, expected)

from django.test import override_settings
from unittest import mock
from django.test import SimpleTestCase, override_settings
from django.views.debug import SafeExceptionReporterFilter, CallableSettingWrapper

class CleanseListTupleRegressionTests(SimpleTestCase):

    def setUp(self):
        self.filter = SafeExceptionReporterFilter()
        self.sub = self.filter.cleansed_substitute

from django.test import SimpleTestCase
from django.views.debug import SafeExceptionReporterFilter, CallableSettingWrapper

class ListTupleCleanseTests(SimpleTestCase):

    def setUp(self):
        self.filter = SafeExceptionReporterFilter()
        self.stars = self.filter.cleansed_substitute

from django.test import SimpleTestCase
from django.views.debug import SafeExceptionReporterFilter

class CleanseSettingListTupleRegressionTests(SimpleTestCase):

    def setUp(self):
        self.filter = SafeExceptionReporterFilter()

from django.views.debug import SafeExceptionReporterFilter, CallableSettingWrapper
from django.test import SimpleTestCase, override_settings
from unittest import mock
from django.test import SimpleTestCase, override_settings
from django.views.debug import SafeExceptionReporterFilter, CallableSettingWrapper
from django.conf import settings

class CleanseListTupleRegressionTests(SimpleTestCase):

    def setUp(self):
        self.filter = SafeExceptionReporterFilter()

from django.test import SimpleTestCase
from django.views.debug import SafeExceptionReporterFilter, CallableSettingWrapper

from django.test import SimpleTestCase
from django.views.debug import SafeExceptionReporterFilter, CallableSettingWrapper

class SafeExceptionReporterFilterListTupleTests(SimpleTestCase):

    def setUp(self):
        self.filter = SafeExceptionReporterFilter()

from collections import namedtuple
from django.test import SimpleTestCase
from django.views.debug import SafeExceptionReporterFilter
from collections import namedtuple
from django.test import SimpleTestCase
from django.views.debug import SafeExceptionReporterFilter

class ListTupleSubclassTests(SimpleTestCase):

    def setUp(self):
        self.filter = SafeExceptionReporterFilter()
        self.sub = self.filter.cleansed_substitute

    def test_namedtuple_tuple_handling_sensitive_inner(self):
        NT = namedtuple('NT', ['a', 'b'])
        nt = NT({'API_KEY': 'k'}, {'name': 'app'})
        result = self.filter.cleanse_setting('MY_SETTING', nt)
        self.assertEqual(result, ({'API_KEY': self.sub}, {'name': 'app'}))

    def test_namedtuple_mixed_nested_structures(self):
        NT = namedtuple('NT', ['left', 'right'])
        nt = NT([{'SECRET_KEY': 's'}], ('plain', {'TOKEN': 't'}))
        result = self.filter.cleanse_setting('MY_SETTING', nt)
        self.assertEqual(result, ([{'SECRET_KEY': self.sub}], ('plain', {'TOKEN': self.sub})))

    def test_tuple_namedtuple_non_string_inner_key(self):
        NT = namedtuple('NT', ['a'])
        nt = NT({42: 'value'})
        result = self.filter.cleanse_setting('MY_SETTING', nt)
        self.assertEqual(result, ({42: 'value'},))