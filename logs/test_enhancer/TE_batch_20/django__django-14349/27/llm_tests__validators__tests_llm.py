# No additional imports required beyond those in test_code.
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from django.test import SimpleTestCase

class URLValidatorUnsafeCharsTests(SimpleTestCase):
    def test_subclass_custom_unsafe_in_userinfo(self):
        class CustomURLValidator(URLValidator):
            unsafe_chars = frozenset('!')

        validator = CustomURLValidator()
        with self.assertRaises(ValidationError):
            validator('http://user!name@example.com/')

    def test_instance_custom_unsafe_in_userinfo(self):
        validator = URLValidator()
        validator.unsafe_chars = frozenset('!')
        with self.assertRaises(ValidationError):
            validator('http://user!name@example.com/')

    def test_subclass_custom_unsafe_in_path(self):
        class CustomURLValidator(URLValidator):
            unsafe_chars = frozenset('!')

        validator = CustomURLValidator()
        with self.assertRaises(ValidationError):
            validator('http://example.com/path!more')

    def test_subclass_custom_unsafe_in_query(self):
        class CustomURLValidator(URLValidator):
            unsafe_chars = frozenset('!')

        validator = CustomURLValidator()
        with self.assertRaises(ValidationError):
            validator('http://example.com/?q=bad!')

    def test_subclass_custom_unsafe_in_fragment(self):
        class CustomURLValidator(URLValidator):
            unsafe_chars = frozenset('!')

        validator = CustomURLValidator()
        with self.assertRaises(ValidationError):
            validator('http://example.com/#frag!')

    def test_multiple_custom_unsafe_chars(self):
        class CustomURLValidator(URLValidator):
            unsafe_chars = frozenset('!$')

        validator = CustomURLValidator()
        with self.assertRaises(ValidationError):
            validator('http://example.com/price$99')

    def test_unicode_custom_unsafe_char(self):
        # Unicode characters must also be honored via unsafe_chars
        class CustomURLValidator(URLValidator):
            unsafe_chars = frozenset('✓')

        validator = CustomURLValidator()
        with self.assertRaises(ValidationError):
            validator('http://example.com/ok✓')

    def test_instance_override_respected_for_path(self):
        validator = URLValidator()
        validator.unsafe_chars = frozenset('*')
        with self.assertRaises(ValidationError):
            validator('http://example.com/contains*star')

    def test_custom_unsafe_in_query_with_instance_override(self):
        validator = URLValidator()
        validator.unsafe_chars = frozenset('@!')
        with self.assertRaises(ValidationError):
            validator('http://example.com/?a=value!')

    def test_custom_unsafe_digit_in_path(self):
        class CustomURLValidator(URLValidator):
            # Unusual: disallow a digit character via unsafe_chars
            unsafe_chars = frozenset('9')

        validator = CustomURLValidator()
        with self.assertRaises(ValidationError):
            validator('http://example.com/has9digit')

from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from django.test import SimpleTestCase

class URLValidatorUnsafeCharsTests(SimpleTestCase):

    def test_class_has_unsafe_chars_attribute(self):
        self.assertTrue(hasattr(URLValidator, 'unsafe_chars'))
        self.assertEqual(URLValidator.unsafe_chars, frozenset('\t\r\n'))

    def test_instance_has_unsafe_chars_attribute(self):
        validator = URLValidator()
        self.assertTrue(hasattr(validator, 'unsafe_chars'))
        self.assertEqual(validator.unsafe_chars, URLValidator.unsafe_chars)

    def test_unsafe_chars_contains_expected_characters(self):
        for ch in ('\t', '\r', '\n'):
            self.assertIn(ch, URLValidator.unsafe_chars)

    def test_unsafe_chars_intersection_detects_newline(self):
        self.assertTrue(URLValidator.unsafe_chars.intersection('http://example.com/\n'))

    def test_monkeypatch_remove_tab_allows_tab_in_url(self):
        original = URLValidator.unsafe_chars
        try:
            URLValidator.unsafe_chars = frozenset('\r\n')
            validator = URLValidator()
            self.assertIsNone(validator('http://example.com/\t'))
        finally:
            URLValidator.unsafe_chars = original

    def test_monkeypatch_add_custom_unsafe_character_rejects_it(self):
        original = URLValidator.unsafe_chars
        try:
            URLValidator.unsafe_chars = frozenset('!')
            validator = URLValidator()
            with self.assertRaises(ValidationError):
                validator('http://example.com/!')
            self.assertIsNone(validator('http://example.com/\t'))
        finally:
            URLValidator.unsafe_chars = original

    def test_instance_level_unsafe_chars_override(self):
        original = URLValidator.unsafe_chars
        try:
            v = URLValidator()
            v.unsafe_chars = frozenset('!')
            with self.assertRaises(ValidationError):
                v('http://example.com/!')
            self.assertIsNone(v('http://example.com/\t'))
        finally:
            URLValidator.unsafe_chars = original

    def test_subclass_override_changes_behavior(self):
        original = URLValidator.unsafe_chars
        try:

            class BangURLValidator(URLValidator):
                unsafe_chars = frozenset('!')
            v = BangURLValidator()
            with self.assertRaises(ValidationError):
                v('http://example.com/!')
            self.assertTrue(URLValidator.unsafe_chars.intersection('http://x\n'))
        finally:
            URLValidator.unsafe_chars = original

    def test_setting_unsafe_chars_to_empty_allows_tab_and_newline(self):
        original = URLValidator.unsafe_chars
        try:
            URLValidator.unsafe_chars = frozenset()
            validator = URLValidator()
            self.assertIsNone(validator('http://example.com/\t'))
            self.assertIsNone(validator('http://example.com/\n'))
        finally:
            URLValidator.unsafe_chars = original

from django.core.exceptions import ValidationError
from django.test import SimpleTestCase
from django.core.validators import URLValidator

class URLValidatorUnsafeCharsTests(SimpleTestCase):

    def test_unsafe_chars_attribute_exists(self):
        self.assertTrue(hasattr(URLValidator, 'unsafe_chars'))
        unsafe = URLValidator.unsafe_chars
        self.assertIsInstance(unsafe, frozenset)

    def test_unsafe_chars_contains_tab_cr_lf(self):
        unsafe = URLValidator.unsafe_chars
        self.assertIn('\t', unsafe)
        self.assertIn('\r', unsafe)
        self.assertIn('\n', unsafe)
        self.assertNotIn(' ', unsafe)

    def test_space_is_not_considered_unsafe(self):
        self.assertNotIn(' ', URLValidator.unsafe_chars)
        validator = URLValidator()
        with self.assertRaises(ValidationError):
            validator('http://example.com/ ')

    def test_unsafe_chars_is_immutable_frozenset(self):
        unsafe = URLValidator.unsafe_chars
        self.assertEqual(type(unsafe), frozenset)
        with self.assertRaises(AttributeError):
            unsafe.add('x')

from django.test import SimpleTestCase
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from django.test import SimpleTestCase
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

class URLUnsafeCharsTests(SimpleTestCase):

    def test_unsafe_chars_class_attribute(self):
        self.assertTrue(hasattr(URLValidator, 'unsafe_chars'))
        self.assertIsInstance(URLValidator.unsafe_chars, frozenset)
        self.assertEqual(URLValidator.unsafe_chars, frozenset('\t\r\n'))

    def test_unsafe_chars_instance_attribute(self):
        v = URLValidator()
        self.assertTrue(hasattr(v, 'unsafe_chars'))
        self.assertIsInstance(v.unsafe_chars, frozenset)
        self.assertEqual(v.unsafe_chars, frozenset('\t\r\n'))

    def test_newline_detected_and_rejected(self):
        v = URLValidator()
        url = 'http://example.com/\n'
        self.assertEqual(v.unsafe_chars.intersection(url), {'\n'})
        with self.assertRaises(ValidationError):
            v(url)

    def test_carriage_return_detected_and_rejected(self):
        v = URLValidator()
        url = 'http://example.com/\r'
        self.assertEqual(v.unsafe_chars.intersection(url), {'\r'})
        with self.assertRaises(ValidationError):
            v(url)

    def test_tab_detected_and_rejected(self):
        v = URLValidator()
        url = 'http://\texample.com/'
        self.assertEqual(v.unsafe_chars.intersection(url), {'\t'})
        with self.assertRaises(ValidationError):
            v(url)

    def test_newline_in_scheme_rejected(self):
        v = URLValidator()
        url = 'http\n://example.com/'
        self.assertEqual(v.unsafe_chars.intersection(url), {'\n'})
        with self.assertRaises(ValidationError):
            v(url)

    def test_newline_at_start_rejected(self):
        v = URLValidator()
        url = '\nhttp://example.com/'
        self.assertEqual(v.unsafe_chars.intersection(url), {'\n'})
        with self.assertRaises(ValidationError):
            v(url)

    def test_newline_in_userinfo_rejected(self):
        v = URLValidator()
        url = 'http://user\n:pass@example.com/'
        self.assertEqual(v.unsafe_chars.intersection(url), {'\n'})
        with self.assertRaises(ValidationError):
            v(url)

    def test_newline_after_ipv6_host_rejected(self):
        v = URLValidator()
        url = 'http://[::ffff:127.0.0.1]\n'
        self.assertEqual(v.unsafe_chars.intersection(url), {'\n'})
        with self.assertRaises(ValidationError):
            v(url)

from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from django.test import SimpleTestCase
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from django.test import SimpleTestCase

class URLValidatorUnsafeCharsTests(SimpleTestCase):

    def test_unsafe_chars_attribute_exists(self):
        self.assertTrue(hasattr(URLValidator, 'unsafe_chars'))
        self.assertEqual(URLValidator.unsafe_chars, frozenset('\t\r\n'))

from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from django.test import SimpleTestCase


class URLValidatorCustomUnsafeCharsTests(SimpleTestCase):
    def test_pipe_in_path(self):
        v = URLValidator()
        v.unsafe_chars = frozenset('|')
        with self.assertRaises(ValidationError):
            v('http://example.com/pa|th')

    def test_semicolon_in_path(self):
        v = URLValidator()
        v.unsafe_chars = frozenset(';')
        with self.assertRaises(ValidationError):
            v('http://example.com/a;b')

    def test_percent_in_path(self):
        v = URLValidator()
        v.unsafe_chars = frozenset('%')
        with self.assertRaises(ValidationError):
            v('http://example.com/%2F')

    def test_emoji_in_path(self):
        v = URLValidator()
        v.unsafe_chars = frozenset('😊')
        with self.assertRaises(ValidationError):
            v('http://example.com/😊')

    def test_backtick_in_path(self):
        v = URLValidator()
        v.unsafe_chars = frozenset('`')
        with self.assertRaises(ValidationError):
            v('http://example.com/path`with`backtick')

    def test_pipe_in_userinfo(self):
        v = URLValidator()
        v.unsafe_chars = frozenset('|')
        with self.assertRaises(ValidationError):
            v('http://user|name:pass@example.com/')

    def test_caret_in_fragment(self):
        v = URLValidator()
        v.unsafe_chars = frozenset('^')
        with self.assertRaises(ValidationError):
            v('http://example.com/#frag^ment')

    def test_plus_in_path(self):
        v = URLValidator()
        v.unsafe_chars = frozenset('+')
        with self.assertRaises(ValidationError):
            v('http://example.com/a+b')

    def test_multiple_custom_unsafe_chars(self):
        v = URLValidator()
        v.unsafe_chars = frozenset('|;^')
        with self.assertRaises(ValidationError):
            v('http://example.com/has^char')

    def test_custom_unsafe_char_in_userinfo_and_path(self):
        v = URLValidator()
        # Disallow both ':' and '|' as an example of multiple custom unsafe chars.
        # (':' normally has semantic meaning in userinfo, but this demonstrates
        # that the instance-level unsafe_chars controls validation.)
        v.unsafe_chars = frozenset('|:')
        with self.assertRaises(ValidationError):
            v('http://user|name:pass@example.com/pa|th')

from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from django.test import SimpleTestCase

class CustomUnsafeCharsTests(SimpleTestCase):

    def test_rejects_exclamation_in_path(self):

        class BangValidator(URLValidator):
            unsafe_chars = frozenset('!')
        validator = BangValidator()
        with self.assertRaises(ValidationError):
            validator('http://example.com/path!withbang')

    def test_rejects_exclamation_in_userinfo(self):

        class BangValidator(URLValidator):
            unsafe_chars = frozenset('!')
        validator = BangValidator()
        with self.assertRaises(ValidationError):
            validator('http://user:pa!ss@example.com/')

    def test_rejects_exclamation_in_query(self):

        class BangValidator(URLValidator):
            unsafe_chars = frozenset('!')
        validator = BangValidator()
        with self.assertRaises(ValidationError):
            validator('http://example.com/?q=!')

    def test_rejects_exclamation_in_fragment(self):

        class BangValidator(URLValidator):
            unsafe_chars = frozenset('!')
        validator = BangValidator()
        with self.assertRaises(ValidationError):
            validator('http://example.com/#!')

    def test_default_unsafe_chars_on_class(self):
        self.assertTrue(hasattr(URLValidator, 'unsafe_chars'))
        self.assertIsInstance(URLValidator.unsafe_chars, frozenset)
        self.assertIn('\n', URLValidator.unsafe_chars)
        self.assertIn('\r', URLValidator.unsafe_chars)
        self.assertIn('\t', URLValidator.unsafe_chars)

    def test_custom_validator_rejects_bang_but_default_allows(self):

        class BangValidator(URLValidator):
            unsafe_chars = frozenset('!')
        default = URLValidator()
        self.assertIsNone(default('http://example.com/!'))
        with self.assertRaises(ValidationError):
            BangValidator()('http://example.com/!')

    def test_rejects_hash_in_fragment_when_overridden(self):

        class HashValidator(URLValidator):
            unsafe_chars = frozenset('#')
        v = HashValidator()
        with self.assertRaises(ValidationError):
            v('http://example.com/#fragment')

    def test_rejects_bang_in_multiple_positions(self):

        class BangValidator(URLValidator):
            unsafe_chars = frozenset('!')
        v = BangValidator()
        urls = ['http://example.com/!start', 'http://user:!pass@example.com/', 'http://example.com/path/with!bang?x=1', 'http://example.com/#!frag']
        for url in urls:
            with self.subTest(url=url):
                with self.assertRaises(ValidationError):
                    v(url)

# No additional imports required.
from django.test import SimpleTestCase
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError


class URLValidatorUnsafeCharsTests(SimpleTestCase):

    def test_class_has_unsafe_chars(self):
        # The class should expose an unsafe_chars frozenset with the default
        self.assertTrue(hasattr(URLValidator, 'unsafe_chars'))
        self.assertIsInstance(URLValidator.unsafe_chars, frozenset)
        self.assertEqual(URLValidator.unsafe_chars, frozenset('\t\r\n'))

    def test_instance_unsafe_chars_rejects_exclamation_in_path(self):
        v = URLValidator()
        v.unsafe_chars = frozenset('!')
        with self.assertRaises(ValidationError):
            v('http://example.com/path!')

    def test_instance_unsafe_chars_rejects_exclamation_in_userinfo(self):
        v = URLValidator()
        v.unsafe_chars = frozenset('!')
        # '!' in the userinfo part should be rejected when listed in unsafe_chars
        with self.assertRaises(ValidationError):
            v('http://user!@example.com/')

    def test_instance_unsafe_chars_rejects_hash_in_fragment(self):
        v = URLValidator()
        v.unsafe_chars = frozenset('#')
        # '#' normally introduces the fragment and is allowed syntactically,
        # but should be rejected early if listed in unsafe_chars.
        with self.assertRaises(ValidationError):
            v('http://example.com/path#frag')

    def test_instance_unsafe_chars_rejects_dollar_in_path(self):
        v = URLValidator()
        v.unsafe_chars = frozenset('$')
        with self.assertRaises(ValidationError):
            v('http://example.com/path$more')

    def test_subclass_unsafe_chars_rejects_caret(self):
        class MyValidator(URLValidator):
            unsafe_chars = frozenset('^')

        v = MyValidator()
        with self.assertRaises(ValidationError):
            v('http://example.com/path^')

    def test_subclass_unsafe_chars_rejects_star(self):
        class MyValidator(URLValidator):
            unsafe_chars = frozenset('*')

        v = MyValidator()
        with self.assertRaises(ValidationError):
            v('http://example.com/te*st')

    def test_instance_unsafe_chars_toggle(self):
        v = URLValidator()
        v.unsafe_chars = frozenset('!')
        # Initially should reject
        with self.assertRaises(ValidationError):
            v('http://example.com/path!')
        # After clearing unsafe_chars the same URL should be accepted
        v.unsafe_chars = frozenset()
        self.assertIsNone(v('http://example.com/path!'))

    def test_subclass_combined_unsafe_chars(self):
        class MyValidator(URLValidator):
            unsafe_chars = frozenset('!$#')

        v = MyValidator()
        with self.assertRaises(ValidationError):
            v('http://user!@example.com/')
        with self.assertRaises(ValidationError):
            v('http://example.com/path$more')
        with self.assertRaises(ValidationError):
            v('http://example.com/path#frag')

    def test_setting_unsafe_chars_does_not_affect_other_instances(self):
        v1 = URLValidator()
        v2 = URLValidator()
        v1.unsafe_chars = frozenset('!')
        # v1 rejects because of its instance override
        with self.assertRaises(ValidationError):
            v1('http://example.com/path!')
        # v2 should still accept the URL since it uses the class default
        self.assertIsNone(v2('http://example.com/path!'))

from django.core.exceptions import ValidationError
from django.test import SimpleTestCase
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from django.test import SimpleTestCase
from django.core.validators import URLValidator

class URLValidatorUnsafeCharsTests(SimpleTestCase):

    def test_subclass_unsafe_chars_blocks_custom_char(self):

        class CustomURLValidator(URLValidator):
            unsafe_chars = frozenset({'*'})
        validator = CustomURLValidator()
        with self.assertRaises(ValidationError):
            validator('http://example.com/path*bad')

    def test_subclass_unsafe_chars_combination(self):

        class Custom(URLValidator):
            unsafe_chars = frozenset({'*', ' '})
        v = Custom()
        with self.assertRaises(ValidationError):
            v('http://exa mple.com/')
        with self.assertRaises(ValidationError):
            v('http://example.com/path*')

from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from django.test import SimpleTestCase

class URLValidatorUnsafeCharsTests(SimpleTestCase):
    def test_has_unsafe_chars_attribute(self):
        # The class must expose unsafe_chars so callers can inspect/modify it.
        self.assertTrue(hasattr(URLValidator, 'unsafe_chars'))

    def test_unsafe_chars_is_frozenset(self):
        # It should be a frozenset of characters.
        self.assertIsInstance(URLValidator.unsafe_chars, frozenset)

    def test_default_contains_control_chars(self):
        # Ensure the default unsafe_chars contains the standard control characters.
        for ch in ('\t', '\r', '\n'):
            self.assertIn(ch, URLValidator.unsafe_chars)

    def test_class_attribute_changes_behavior_for_non_whitespace_char(self):
        # Changing the class attribute should affect validation for characters
        # that are not otherwise rejected by the URL regex (e.g. '+').
        original = URLValidator.unsafe_chars
        try:
            URLValidator.unsafe_chars = frozenset(['+'])
            v = URLValidator()
            with self.assertRaises(ValidationError):
                v('http://example.com/has+plus')
        finally:
            URLValidator.unsafe_chars = original

    def test_instance_attribute_override_changes_behavior(self):
        # Overriding the instance attribute should change that instance's behavior.
        v = URLValidator()
        # Ensure instance initially does not reject '+' (unless class changed by other tests).
        # Temporarily set instance unsafe_chars to include '$' and confirm rejection.
        v.unsafe_chars = frozenset(['$'])
        with self.assertRaises(ValidationError):
            v('http://example.com/path$here')

    def test_subclass_inherits_unsafe_chars(self):
        # Subclasses should inherit the unsafe_chars attribute by default.
        class MyValidator(URLValidator):
            pass
        self.assertEqual(MyValidator.unsafe_chars, URLValidator.unsafe_chars)

    def test_modifying_subclass_attribute_does_not_change_base(self):
        # Changing subclass attribute should not mutate the base class attribute.
        class MyValidator(URLValidator):
            pass
        original_base = URLValidator.unsafe_chars
        original_sub = MyValidator.unsafe_chars
        try:
            MyValidator.unsafe_chars = frozenset(['+'])
            self.assertNotEqual(MyValidator.unsafe_chars, URLValidator.unsafe_chars)
        finally:
            URLValidator.unsafe_chars = original_base
            MyValidator.unsafe_chars = original_sub

    def test_subclass_respects_its_own_unsafe_chars(self):
        # A subclass with a custom unsafe_chars should reject characters accordingly.
        class MyValidator(URLValidator):
            pass
        original = MyValidator.unsafe_chars
        try:
            MyValidator.unsafe_chars = frozenset(['%'])
            with self.assertRaises(ValidationError):
                MyValidator()('http://example.com/with%percent')
        finally:
            MyValidator.unsafe_chars = original

    def test_setting_unsafe_chars_to_arbitrary_character(self):
        # Ensure arbitrary (non-whitespace) characters can be used to mark URLs invalid.
        original = URLValidator.unsafe_chars
        try:
            URLValidator.unsafe_chars = frozenset(['Ω'])
            with self.assertRaises(ValidationError):
                URLValidator()('http://example.com/withΩchar')
        finally:
            URLValidator.unsafe_chars = original

    def test_instance_attribute_is_same_object_as_class_by_default(self):
        # By default, an instance should reference the class-level unsafe_chars object.
        v = URLValidator()
        self.assertIs(v.unsafe_chars, URLValidator.unsafe_chars)

from django.core.exceptions import ValidationError
from django.test import SimpleTestCase
from django.core.validators import URLValidator


class TestURLValidatorCustomUnsafeChars(SimpleTestCase):
    def test_subclass_blocks_custom_unsafe_char_in_path(self):
        class V(URLValidator):
            unsafe_chars = frozenset('!')

        with self.assertRaises(ValidationError):
            V()('http://example.com/path!more')

    def test_instance_blocks_custom_unsafe_char_in_path(self):
        v = URLValidator()
        v.unsafe_chars = frozenset('$')
        with self.assertRaises(ValidationError):
            v('http://example.com/path$more')

    def test_subclass_blocks_custom_unsafe_char_in_username(self):
        class V(URLValidator):
            unsafe_chars = frozenset('!')

        with self.assertRaises(ValidationError):
            V()('http://user!name@example.com/')

    def test_instance_blocks_custom_unsafe_char_in_username(self):
        v = URLValidator()
        v.unsafe_chars = frozenset(';')
        with self.assertRaises(ValidationError):
            v('http://user;name@example.com/')

    def test_subclass_blocks_multiple_chars(self):
        class V(URLValidator):
            unsafe_chars = frozenset('!$')

        with self.assertRaises(ValidationError):
            V()('http://example.com/path$')

    def test_instance_attribute_after_init_respected(self):
        v = URLValidator()
        # ensure changing the instance attribute after initialization is respected
        v.unsafe_chars = set('^')
        with self.assertRaises(ValidationError):
            v('http://example.com/^caret')

    def test_custom_unsafe_chars_with_extended_schemes(self):
        class V(URLValidator):
            unsafe_chars = frozenset('%')

        validator = V(schemes=['http', 'https'])
        with self.assertRaises(ValidationError):
            validator('http://example.com/%percent')

    def test_custom_unsafe_chars_blocks_in_query(self):
        v = URLValidator()
        v.unsafe_chars = frozenset('|')
        with self.assertRaises(ValidationError):
            v('http://example.com/path?param=|value')

    def test_custom_unsafe_chars_blocks_in_fragment(self):
        v = URLValidator()
        v.unsafe_chars = frozenset('$')
        with self.assertRaises(ValidationError):
            v('http://example.com/path#section$1')

    def test_subclass_unsafe_chars_allows_other_chars(self):
        class V(URLValidator):
            unsafe_chars = frozenset('!')

        validator = V()
        # '!' should be blocked
        with self.assertRaises(ValidationError):
            validator('http://example.com/has!bang')
        # '?' should still be allowed
        self.assertIsNone(validator('http://example.com/?q=ok'))

from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from unittest import mock
from django.test import SimpleTestCase
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator

class URLValidatorUnsafeCharsTests(SimpleTestCase):

    def test_unsafe_chars_attribute_exists_and_default(self):
        self.assertTrue(hasattr(URLValidator, 'unsafe_chars'))
        self.assertEqual(URLValidator.unsafe_chars, frozenset('\t\r\n'))

    def test_modifying_class_attribute_restored_properly_between_tests(self):
        original = URLValidator.unsafe_chars
        URLValidator.unsafe_chars = frozenset('%')
        URLValidator.unsafe_chars = original
        v = URLValidator()
        with self.assertRaises(ValidationError):
            v('http://example.com/\t')

from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from django.test import SimpleTestCase

class TestURLValidatorUnsafeChars(SimpleTestCase):

    def setUp(self):
        self.validator = URLValidator()

from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from django.test import SimpleTestCase
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from django.test import SimpleTestCase


class URLValidatorUnsafeCharsTests(SimpleTestCase):
    def test_class_override_rejects_pipe_in_path(self):
        class CustomValidator(URLValidator):
            unsafe_chars = frozenset('|')

        v = CustomValidator()
        with self.assertRaises(ValidationError):
            v('http://example.com/path|withpipe')

    def test_instance_override_rejects_pipe_in_path(self):
        v = URLValidator()
        v.unsafe_chars = frozenset('|')
        with self.assertRaises(ValidationError):
            v('http://example.com/path|withpipe')

    def test_mutated_instance_unsafe_chars_after_init(self):
        v = URLValidator()
        # mutate after construction
        v.unsafe_chars = frozenset('|')
        with self.assertRaises(ValidationError):
            v('http://example.com/another|path')

    def test_class_override_rejects_pipe_in_query(self):
        class CustomValidator(URLValidator):
            unsafe_chars = frozenset('|')

        v = CustomValidator()
        with self.assertRaises(ValidationError):
            v('http://example.com/path?query=foo|bar')

    def test_class_override_rejects_pipe_in_fragment(self):
        class CustomValidator(URLValidator):
            unsafe_chars = frozenset('|')

        v = CustomValidator()
        with self.assertRaises(ValidationError):
            v('http://example.com/path#frag|ment')

    def test_class_override_rejects_pipe_in_userinfo(self):
        class CustomValidator(URLValidator):
            unsafe_chars = frozenset('|')

        v = CustomValidator()
        # userinfo (user part) allows '|' in the regex, so custom unsafe_chars should reject it
        with self.assertRaises(ValidationError):
            v('http://user|name:password@example.com/')

    def test_multiple_unsafe_chars_rejected(self):
        class CustomValidator(URLValidator):
            unsafe_chars = frozenset({'|', ';'})

        v = CustomValidator()
        with self.assertRaises(ValidationError):
            v('http://example.com/path;params')
        with self.assertRaises(ValidationError):
            v('http://example.com/path|params')

    def test_caret_rejected_when_configured(self):
        class CustomValidator(URLValidator):
            unsafe_chars = frozenset('^')

        v = CustomValidator()
        with self.assertRaises(ValidationError):
            v('http://example.com/abc^def')

    def test_underscore_rejected_when_configured(self):
        class CustomValidator(URLValidator):
            unsafe_chars = frozenset('_')

        v = CustomValidator()
        # underscore in the path is normally allowed by the URL regex,
        # but should be rejected if declared unsafe.
        with self.assertRaises(ValidationError):
            v('http://example.com/abc_def')

    def test_changing_class_attribute_affects_all_instances(self):
        original = URLValidator.unsafe_chars
        try:
            URLValidator.unsafe_chars = frozenset('|')
            v = URLValidator()
            with self.assertRaises(ValidationError):
                v('http://example.com/pipe|here')
        finally:
            # restore to avoid leaking state to other tests
            URLValidator.unsafe_chars = original

from django.test import SimpleTestCase
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator

class URLValidatorUnsafeCharsTests(SimpleTestCase):

    def test_unsafe_chars_attribute_present(self):
        self.assertTrue(hasattr(URLValidator, 'unsafe_chars'))

    def test_unsafe_chars_is_frozenset_and_default_members(self):
        self.assertIsInstance(URLValidator.unsafe_chars, frozenset)
        self.assertSetEqual(set(URLValidator.unsafe_chars), set('\t\r\n'))

    def test_instance_override_rejects_dollar_in_path(self):
        v = URLValidator()
        v.unsafe_chars = set('$')
        with self.assertRaises(ValidationError):
            v('http://example.com/path$end')

    def test_instance_override_rejects_at_in_userinfo(self):
        v = URLValidator()
        v.unsafe_chars = set('@')
        with self.assertRaises(ValidationError):
            v('http://user:pass@example.com/')

    def test_class_override_rejects_percent_in_fragment(self):
        original = URLValidator.unsafe_chars
        try:
            URLValidator.unsafe_chars = set('%')
            v = URLValidator()
            with self.assertRaises(ValidationError):
                v('http://example.com/#%20')
        finally:
            URLValidator.unsafe_chars = original

    def test_subclass_override_rejects_hash_in_fragment(self):

        class MyValidator(URLValidator):
            unsafe_chars = set('#')
        v = MyValidator()
        with self.assertRaises(ValidationError):
            v('http://example.com/#fragment')

    def test_multiple_chars_in_unsafe_chars(self):
        v = URLValidator()
        v.unsafe_chars = set('!$')
        with self.assertRaises(ValidationError):
            v('http://example.com/hello!')

    def test_setting_unsafe_chars_affects_new_instances(self):
        original = URLValidator.unsafe_chars
        try:
            URLValidator.unsafe_chars = set('^')
            v = URLValidator()
            with self.assertRaises(ValidationError):
                v('http://example.com/path^oops')
        finally:
            URLValidator.unsafe_chars = original

    def test_subclass_custom_unsafe_chars_rejects_multiple(self):

        class Sub2(URLValidator):
            unsafe_chars = set(['$', '%'])
        v = Sub2()
        with self.assertRaises(ValidationError):
            v('http://example.com/$and%')

# No new imports beyond standard testing helpers are required.
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from django.test import SimpleTestCase


class URLUnsafeCharsTests(SimpleTestCase):
    def test_unsafe_chars_attribute_exists(self):
        # The class should define the unsafe_chars attribute.
        self.assertTrue(hasattr(URLValidator, 'unsafe_chars'))
        self.assertIsInstance(URLValidator.unsafe_chars, frozenset)

    def test_unsafe_chars_default_contents(self):
        # Default should be the three characters: tab, carriage return and newline.
        self.assertEqual(URLValidator.unsafe_chars, frozenset('\t\r\n'))

    def test_instance_override_blocks_char_in_path(self):
        # Instance-level override should be respected.
        validator = URLValidator()
        original = URLValidator.unsafe_chars
        try:
            # Add '!' as an unsafe character on the instance.
            validator.unsafe_chars = frozenset('!')
            with self.assertRaises(ValidationError):
                validator('http://example.com/path!withchar')
        finally:
            URLValidator.unsafe_chars = original

    def test_class_override_blocks_char_in_path(self):
        # Class-level override should be respected for newly created instances.
        original = URLValidator.unsafe_chars
        try:
            URLValidator.unsafe_chars = frozenset('!')
            validator = URLValidator()
            with self.assertRaises(ValidationError):
                validator('http://example.com/path!char')
        finally:
            URLValidator.unsafe_chars = original

    def test_instance_override_precedence_over_class(self):
        # Instance-level unsafe_chars should take precedence over class-level value.
        original = URLValidator.unsafe_chars
        try:
            # Make class allow everything (empty set)
            URLValidator.unsafe_chars = frozenset()
            # But instance marks '!' as unsafe
            validator = URLValidator()
            validator.unsafe_chars = frozenset('!')
            # instance should reject
            with self.assertRaises(ValidationError):
                validator('http://example.com/path!char')
            # another instance without override should accept the same URL
            other = URLValidator()
            # Should not raise because class unsafe_chars is empty
            other('http://example.com/path!char')
        finally:
            URLValidator.unsafe_chars = original

    def test_setting_unsafe_chars_to_multiple_chars(self):
        original = URLValidator.unsafe_chars
        try:
            validator = URLValidator()
            validator.unsafe_chars = frozenset('!$')
            with self.assertRaises(ValidationError):
                validator('http://example.com/foo$bar')
            with self.assertRaises(ValidationError):
                validator('http://example.com/foo!bar')
        finally:
            URLValidator.unsafe_chars = original

    def test_unsafe_chars_is_frozenset_type(self):
        # Ensure the attribute is a frozenset (immutable set-like type)
        self.assertIsInstance(URLValidator.unsafe_chars, frozenset)

    def test_modifying_unsafe_chars_restored(self):
        # Ensure we can change and restore the class attribute without side-effects
        original = URLValidator.unsafe_chars
        URLValidator.unsafe_chars = frozenset('!')
        self.assertEqual(URLValidator.unsafe_chars, frozenset('!'))
        # restore
        URLValidator.unsafe_chars = original
        self.assertEqual(URLValidator.unsafe_chars, original)

    def test_class_override_applies_to_new_instances(self):
        original = URLValidator.unsafe_chars
        try:
            URLValidator.unsafe_chars = frozenset('%')
            new_validator = URLValidator()
            with self.assertRaises(ValidationError):
                new_validator('http://example.com/percent%sign')
        finally:
            URLValidator.unsafe_chars = original

    def test_instance_has_unsafe_chars_attribute_even_for_non_str_input(self):
        # Non-str input should raise ValidationError before unsafe char checks,
        # but instance should still expose the attribute.
        validator = URLValidator()
        self.assertTrue(hasattr(validator, 'unsafe_chars'))
        with self.assertRaises(ValidationError):
            validator(123)

from django.test import SimpleTestCase
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

class URLUnsafeCharsCustomizationTests(SimpleTestCase):
    def setUp(self):
        # Preserve the original class attribute so tests don't leak state.
        self._orig_class_unsafe = URLValidator.unsafe_chars

    def tearDown(self):
        URLValidator.unsafe_chars = self._orig_class_unsafe

    def test_instance_custom_unsafe_char_rejected(self):
        v = URLValidator()
        # Use vertical tab (not in the default set of \t, \r, \n)
        v.unsafe_chars = frozenset('\x0b')
        with self.assertRaises(ValidationError):
            v('http://example.com/\x0b')

    def test_class_custom_unsafe_char_rejected(self):
        # Set at the class level and ensure the instance reflects it.
        URLValidator.unsafe_chars = frozenset('\x0b')
        v = URLValidator()
        with self.assertRaises(ValidationError):
            v('http://example.com/\x0b')

    def test_instance_multiple_custom_chars(self):
        v = URLValidator()
        v.unsafe_chars = frozenset('\x0b!')
        with self.assertRaises(ValidationError):
            v('http://example.com/!')

    def test_custom_unsafe_char_in_userinfo(self):
        v = URLValidator()
        v.unsafe_chars = frozenset('\x0b')
        # Character in the userinfo (before @) should be detected.
        with self.assertRaises(ValidationError):
            v('http://user\x0b:pass@example.com/')

    def test_custom_unsafe_char_in_scheme(self):
        v = URLValidator()
        v.unsafe_chars = frozenset('\x0b')
        # Character in the scheme portion should be detected.
        with self.assertRaises(ValidationError):
            v('htt\x0bp://example.com/')

    def test_instance_clearing_unsafe_chars_allows_newlines(self):
        v = URLValidator()
        # Clear the unsafe_chars set; newline should then be allowed.
        v.unsafe_chars = frozenset()
        # Under the gold patch this should NOT raise. The candidate patch
        # still checks for '\n' literally and will raise, causing failure.
        self.assertIsNone(v('http://example.com/\n'))

    def test_unicode_line_separator_custom(self):
        v = URLValidator()
        # Use Unicode line separator (U+2028) as a custom unsafe character.
        v.unsafe_chars = frozenset('\u2028')
        with self.assertRaises(ValidationError):
            v('http://example.com/\u2028')

    def test_custom_only_rejects_only_specified_chars(self):
        v = URLValidator()
        # Only vertical tab is considered unsafe; newline should be allowed.
        v.unsafe_chars = frozenset('\x0b')
        self.assertIsNone(v('http://example.com/\n'))

    def test_subclass_override(self):
        class MyURLValidator(URLValidator):
            unsafe_chars = frozenset('\x0b')

        v = MyURLValidator()
        with self.assertRaises(ValidationError):
            v('http://example.com/\x0b')

    def test_restoring_class_attribute_after_modification(self):
        # Modify class attribute and then ensure tearDown restores it.
        URLValidator.unsafe_chars = frozenset('\x0b')
        v = URLValidator()
        with self.assertRaises(ValidationError):
            v('http://example.com/\x0b')
        # After tearDown this will be restored; we just assert the attribute was changed now.
        self.assertEqual(URLValidator.unsafe_chars, frozenset('\x0b'))

from django.test import SimpleTestCase
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

class URLValidatorUnsafeCharsTests(SimpleTestCase):

    def test_class_has_unsafe_chars_attribute(self):
        self.assertTrue(hasattr(URLValidator, 'unsafe_chars'))

    def test_instance_has_unsafe_chars_attribute(self):
        validator = URLValidator()
        self.assertTrue(hasattr(validator, 'unsafe_chars'))

    def test_unsafe_chars_is_frozenset(self):
        self.assertIsInstance(URLValidator.unsafe_chars, frozenset)

    def test_unsafe_chars_contains_tab_cr_lf(self):
        u = URLValidator.unsafe_chars
        self.assertIn('\t', u)
        self.assertIn('\r', u)
        self.assertIn('\n', u)

    def test_unsafe_chars_shared_between_instances(self):
        a = URLValidator()
        b = URLValidator()
        self.assertIs(URLValidator.unsafe_chars, a.unsafe_chars)
        self.assertIs(a.unsafe_chars, b.unsafe_chars)

    def test_unsafe_chars_intersection_detects_forbidden_char(self):
        s = 'http://example.com/\n'
        self.assertTrue(URLValidator.unsafe_chars.intersection(s))

    def test_getattr_accessible(self):
        val = getattr(URLValidator, 'unsafe_chars')
        self.assertIsInstance(val, frozenset)

    def test_subclass_inherits_unsafe_chars(self):

        class SubValidator(URLValidator):
            pass
        self.assertIs(SubValidator.unsafe_chars, URLValidator.unsafe_chars)

    def test_subclass_can_override_unsafe_chars(self):
        custom = frozenset('!')

        class CustomValidator(URLValidator):
            unsafe_chars = custom
        self.assertIs(CustomValidator.unsafe_chars, custom)
        self.assertNotEqual(CustomValidator.unsafe_chars, URLValidator.unsafe_chars)

from django.core.exceptions import ValidationError
from django.test import SimpleTestCase
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from django.test import SimpleTestCase
from django.core.validators import URLValidator

class TestURLValidatorCustomUnsafeChars(SimpleTestCase):

    def test_semicolon_in_path(self):
        self.assert_unsafe_char_rejected('http://example.com/foo;bar', ';')

    def test_semicolon_in_query(self):
        self.assert_unsafe_char_rejected('http://example.com/?a=1;b=2', ';')

    def test_semicolon_in_fragment(self):
        self.assert_unsafe_char_rejected('http://example.com/#frag;ment', ';')

    def test_semicolon_in_userinfo(self):
        self.assert_unsafe_char_rejected('http://user;name:pass@example.com/', ';')

    def test_pipe_in_path(self):
        self.assert_unsafe_char_rejected('http://example.com/foo|bar', '|')

    def test_pipe_in_query(self):
        self.assert_unsafe_char_rejected('http://example.com/?a=1|b=2', '|')

    def test_pipe_in_fragment(self):
        self.assert_unsafe_char_rejected('http://example.com/#frag|ment', '|')

    def test_pipe_in_userinfo(self):
        self.assert_unsafe_char_rejected('http://user|name:pass@example.com/', '|')

    def test_caret_in_path(self):
        self.assert_unsafe_char_rejected('http://example.com/foo^bar', '^')

    def test_caret_in_userinfo(self):
        self.assert_unsafe_char_rejected('http://user^name:pass@example.com/', '^')

from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from django.test import SimpleTestCase

class URLValidatorUnsafeCharsTests(SimpleTestCase):

    def test_has_unsafe_chars_attribute(self):
        self.assertTrue(hasattr(URLValidator, 'unsafe_chars'))
        self.assertEqual(URLValidator.unsafe_chars, frozenset('\t\r\n'))

    def test_unsafe_chars_is_frozenset_and_immutable(self):
        self.assertIsInstance(URLValidator.unsafe_chars, frozenset)
        with self.assertRaises(AttributeError):
            URLValidator.unsafe_chars.add('x')

from unittest import mock
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from django.test import SimpleTestCase

class URLUnsafeCharsTests(SimpleTestCase):

    def setUp(self):
        self.validator = URLValidator()

    def test_unsafe_chars_attribute_exists(self):
        self.assertTrue(hasattr(URLValidator, 'unsafe_chars'))
        self.assertEqual(URLValidator.unsafe_chars, frozenset('\t\r\n'))

    def test_subclass_of_str_hiding_contains_still_rejected(self):

        class SneakyStr(str):

            def __contains__(self, item):
                if item in ('\r', '\n', '\t'):
                    return False
                return super().__contains__(item)
        sneaky = SneakyStr('http://example.com/\n')
        with self.assertRaises(ValidationError):
            self.validator(sneaky)