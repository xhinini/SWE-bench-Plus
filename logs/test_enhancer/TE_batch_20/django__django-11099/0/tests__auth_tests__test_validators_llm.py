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