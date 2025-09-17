import re
from django.test import SimpleTestCase
from django.contrib.auth import validators
import re

class UsernameValidatorRegexTests(SimpleTestCase):

    def test_ascii_regex_exact(self):
        self.assertEqual(validators.ASCIIUsernameValidator.regex, '^[\\w.@+-]+\\Z')

    def test_unicode_regex_exact(self):
        self.assertEqual(validators.UnicodeUsernameValidator.regex, '^[\\w.@+-]+\\Z')

    def test_ascii_regex_startswith_caret(self):
        self.assertTrue(validators.ASCIIUsernameValidator.regex.startswith('^'))

    def test_unicode_regex_startswith_caret(self):
        self.assertTrue(validators.UnicodeUsernameValidator.regex.startswith('^'))

    def test_ascii_regex_does_not_use_backslash_A(self):
        self.assertNotIn('\\A', validators.ASCIIUsernameValidator.regex)

    def test_unicode_regex_does_not_use_backslash_A(self):
        self.assertNotIn('\\A', validators.UnicodeUsernameValidator.regex)

from django.contrib.auth import validators
from django.core.exceptions import ValidationError
from django.test import SimpleTestCase
from django.contrib.auth import validators
from django.core.exceptions import ValidationError
from django.test import SimpleTestCase

class AdditionalUsernameValidatorTests(SimpleTestCase):

    def test_ascii_regex_starts_with_caret(self):
        self.assertTrue(isinstance(validators.ASCIIUsernameValidator.regex, str), 'Expected ASCIIUsernameValidator.regex to be a string.')
        self.assertTrue(validators.ASCIIUsernameValidator.regex.startswith('^'), "ASCIIUsernameValidator.regex must start with '^'.")

    def test_unicode_regex_starts_with_caret(self):
        self.assertTrue(isinstance(validators.UnicodeUsernameValidator.regex, str), 'Expected UnicodeUsernameValidator.regex to be a string.')
        self.assertTrue(validators.UnicodeUsernameValidator.regex.startswith('^'), "UnicodeUsernameValidator.regex must start with '^'.")

from django.test import SimpleTestCase
from django.core.exceptions import ValidationError
from django.contrib import auth
from django.contrib.auth import validators
import re

class UsernameValidatorRegexTests(SimpleTestCase):

    def test_ascii_validator_regex_exact(self):
        self.assertEqual(validators.ASCIIUsernameValidator.regex, '^[\\w.@+-]+\\Z')

    def test_unicode_validator_regex_exact(self):
        self.assertEqual(validators.UnicodeUsernameValidator.regex, '^[\\w.@+-]+\\Z')

    def test_ascii_regex_starts_with_caret(self):
        self.assertTrue(validators.ASCIIUsernameValidator.regex.startswith('^'))

    def test_unicode_regex_starts_with_caret(self):
        self.assertTrue(validators.UnicodeUsernameValidator.regex.startswith('^'))

    def test_ascii_regex_does_not_use_capital_a_anchor(self):
        self.assertNotIn('\\A', validators.ASCIIUsernameValidator.regex)

    def test_unicode_regex_does_not_use_capital_a_anchor(self):
        self.assertNotIn('\\A', validators.UnicodeUsernameValidator.regex)

from django.core.exceptions import ValidationError
from django.test import SimpleTestCase
import re
from django.contrib.auth import validators
from django.core.exceptions import ValidationError
from django.test import SimpleTestCase
import re
from django.contrib.auth import validators

class UsernameRegexAnchorsTests(SimpleTestCase):

    def test_ascii_regex_exact(self):
        self.assertEqual(validators.ASCIIUsernameValidator.regex, '^[\\w.@+-]+\\Z')

    def test_unicode_regex_exact(self):
        self.assertEqual(validators.UnicodeUsernameValidator.regex, '^[\\w.@+-]+\\Z')

    def test_ascii_regex_startswith_caret(self):
        self.assertTrue(validators.ASCIIUsernameValidator.regex.startswith('^'))

    def test_unicode_regex_startswith_caret(self):
        self.assertTrue(validators.UnicodeUsernameValidator.regex.startswith('^'))

    def test_ascii_regex_not_using_backslashA(self):
        self.assertNotIn('\\A', validators.ASCIIUsernameValidator.regex)

    def test_unicode_regex_not_using_backslashA(self):
        self.assertNotIn('\\A', validators.UnicodeUsernameValidator.regex)

from django.test import SimpleTestCase
from django.contrib.auth import validators
from django.core.exceptions import ValidationError

class UsernameValidatorRegressionTests(SimpleTestCase):

    def test_ascii_regex_starts_with_caret(self):
        self.assertTrue(isinstance(validators.ASCIIUsernameValidator.regex, str) and validators.ASCIIUsernameValidator.regex.startswith('^'), msg="ASCIIUsernameValidator.regex must start with '^'")

    def test_unicode_regex_starts_with_caret(self):
        self.assertTrue(isinstance(validators.UnicodeUsernameValidator.regex, str) and validators.UnicodeUsernameValidator.regex.startswith('^'), msg="UnicodeUsernameValidator.regex must start with '^'")

from django.test import SimpleTestCase
from django.contrib.auth import validators
import re
from django.test import SimpleTestCase
from django.contrib.auth import validators
import re

class UsernameRegexAnchorsTests(SimpleTestCase):

    def test_ascii_class_regex_exact(self):
        expected = '^[\\w.@+-]+\\Z'
        self.assertEqual(validators.ASCIIUsernameValidator.regex, expected)

    def test_unicode_class_regex_exact(self):
        expected = '^[\\w.@+-]+\\Z'
        self.assertEqual(validators.UnicodeUsernameValidator.regex, expected)

    def test_ascii_compiled_pattern_matches_exact_string(self):
        expected = '^[\\w.@+-]+\\Z'
        pattern = re.compile(validators.ASCIIUsernameValidator.regex, validators.ASCIIUsernameValidator.flags)
        self.assertEqual(pattern.pattern, expected)

    def test_unicode_compiled_pattern_matches_exact_string(self):
        expected = '^[\\w.@+-]+\\Z'
        pattern = re.compile(validators.UnicodeUsernameValidator.regex, validators.UnicodeUsernameValidator.flags)
        self.assertEqual(pattern.pattern, expected)

    def test_ascii_regex_starts_with_caret(self):
        regex = validators.ASCIIUsernameValidator.regex
        self.assertTrue(regex.startswith('^'))
        self.assertFalse(regex.startswith('\\A'))

    def test_unicode_regex_starts_with_caret(self):
        regex = validators.UnicodeUsernameValidator.regex
        self.assertTrue(regex.startswith('^'))
        self.assertFalse(regex.startswith('\\A'))