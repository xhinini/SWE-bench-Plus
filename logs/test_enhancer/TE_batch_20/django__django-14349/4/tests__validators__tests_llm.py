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