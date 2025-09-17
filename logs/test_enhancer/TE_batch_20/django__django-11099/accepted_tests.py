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

from django.core.exceptions import ValidationError
from django.test import SimpleTestCase
from django.contrib.auth import validators
from django.core.exceptions import ValidationError
from django.test import SimpleTestCase
from django.contrib.auth import validators

class AdditionalUsernameValidatorTests(SimpleTestCase):

    def setUp(self):
        self.ascii_validator = validators.ASCIIUsernameValidator()
        self.unicode_validator = validators.UnicodeUsernameValidator()

from django.core.exceptions import ValidationError
from django.test import SimpleTestCase
from django.contrib.auth import validators
from django.core.exceptions import ValidationError
from django.test import SimpleTestCase

class RegressionUsernameValidatorsTests(SimpleTestCase):

    def test_ascii_regex_string_is_using_backslash_Z_and_caret(self):
        self.assertEqual(validators.ASCIIUsernameValidator.regex, '^[\\w.@+-]+\\Z')

    def test_unicode_regex_string_is_using_backslash_Z_and_caret(self):
        self.assertEqual(validators.UnicodeUsernameValidator.regex, '^[\\w.@+-]+\\Z')

import re
from django.core.exceptions import ValidationError
from django.contrib.auth import validators
from django.core.exceptions import ValidationError
from django.test import SimpleTestCase
import re

class UsernameValidatorRegressionTests(SimpleTestCase):

    def test_ascii_validator_regex_literal(self):
        expected = '^[\\w.@+-]+\\Z'
        self.assertEqual(validators.ASCIIUsernameValidator.regex, expected)

    def test_unicode_validator_regex_literal(self):
        expected = '^[\\w.@+-]+\\Z'
        self.assertEqual(validators.UnicodeUsernameValidator.regex, expected)

import re
import re
from django.test import SimpleTestCase
from django.core.exceptions import ValidationError
from django.contrib.auth import validators

class UsernameMultilineBehaviorTests(SimpleTestCase):

    def test_ascii_multiline_accepts_leading_newline(self):

        class MultiASCII(validators.ASCIIUsernameValidator):
            flags = validators.ASCIIUsernameValidator.flags | re.MULTILINE
        v = MultiASCII()
        self.assertIsNone(v('\ntestuser'))

    def test_ascii_multiline_accepts_middle_newline(self):

        class MultiASCII(validators.ASCIIUsernameValidator):
            flags = validators.ASCIIUsernameValidator.flags | re.MULTILINE
        v = MultiASCII()
        self.assertIsNone(v('prefix\nvaliduser'))

    def test_ascii_multiline_accepts_multiple_newlines_before(self):

        class MultiASCII(validators.ASCIIUsernameValidator):
            flags = validators.ASCIIUsernameValidator.flags | re.MULTILINE
        v = MultiASCII()
        self.assertIsNone(v('a\nb\nvaliduser'))

    def test_unicode_multiline_accepts_leading_newline(self):

        class MultiUnicode(validators.UnicodeUsernameValidator):
            flags = validators.UnicodeUsernameValidator.flags | re.MULTILINE
        v = MultiUnicode()
        self.assertIsNone(v('\nRené'))

    def test_unicode_multiline_accepts_middle_newline(self):

        class MultiUnicode(validators.UnicodeUsernameValidator):
            flags = validators.UnicodeUsernameValidator.flags | re.MULTILINE
        v = MultiUnicode()
        self.assertIsNone(v('prefix\nRené'))

    def test_unicode_multiline_accepts_multiple_newlines_before(self):

        class MultiUnicode(validators.UnicodeUsernameValidator):
            flags = validators.UnicodeUsernameValidator.flags | re.MULTILINE
        v = MultiUnicode()
        self.assertIsNone(v('a\nb\nأحمد'))

import re
import re
from django.test import SimpleTestCase
from django.core.exceptions import ValidationError
from django.contrib.auth import validators

class UsernameValidatorsExtraTests(SimpleTestCase):

    def test_ascii_multiline_accepts_username_on_last_line(self):
        v = validators.ASCIIUsernameValidator(flags=re.MULTILINE)
        self.assertIsNone(v('prefix\nuser123'))

    def test_unicode_multiline_accepts_username_on_last_line(self):
        v = validators.UnicodeUsernameValidator(flags=re.MULTILINE)
        self.assertIsNone(v('prefix\nRené'))

    def test_ascii_multiline_accepts_username_after_multiple_lines(self):
        v = validators.ASCIIUsernameValidator(flags=re.MULTILINE)
        self.assertIsNone(v('a\nb\nfinaluser'))

    def test_unicode_multiline_accepts_username_after_multiple_lines(self):
        v = validators.UnicodeUsernameValidator(flags=re.MULTILINE)
        self.assertIsNone(v('a\nb\nعلي'))

    def test_ascii_multiline_accepts_username_after_crlf(self):
        v = validators.ASCIIUsernameValidator(flags=re.MULTILINE)
        self.assertIsNone(v('prefix\r\nuser_crlf'))

    def test_unicode_multiline_accepts_username_after_crlf(self):
        v = validators.UnicodeUsernameValidator(flags=re.MULTILINE)
        self.assertIsNone(v('prefix\r\nأحمد'))

from django.test import SimpleTestCase
from django.core.exceptions import ValidationError
from django.contrib.auth import validators

class UsernameValidatorRegressionTests(SimpleTestCase):

    def test_ascii_regex_is_caret_and_Z_anchored(self):
        self.assertEqual(validators.ASCIIUsernameValidator.regex, '^[\\w.@+-]+\\Z')

    def test_unicode_regex_is_caret_and_Z_anchored(self):
        self.assertEqual(validators.UnicodeUsernameValidator.regex, '^[\\w.@+-]+\\Z')

from django.contrib.auth import validators
from django.test import SimpleTestCase
from django.core.exceptions import ValidationError
from django.contrib.auth import validators
from django.test import SimpleTestCase
from django.core.exceptions import ValidationError

class UsernameValidatorNewlineRegressionTests(SimpleTestCase):

    def test_ascii_regex_anchor_and_end(self):
        regex = validators.ASCIIUsernameValidator.regex
        self.assertTrue(regex.startswith('^'), 'ASCII regex must start with ^')
        self.assertTrue(regex.endswith('\\Z'), 'ASCII regex must end with \\Z')
        validators.ASCIIUsernameValidator()('glenn')

    def test_unicode_regex_anchor_and_end(self):
        regex = validators.UnicodeUsernameValidator.regex
        self.assertTrue(regex.startswith('^'), 'Unicode regex must start with ^')
        self.assertTrue(regex.endswith('\\Z'), 'Unicode regex must end with \\Z')
        validators.UnicodeUsernameValidator()('René')