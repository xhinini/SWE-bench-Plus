import os
from django.utils.http import http_date

def test_was_modified_since_header_starts_with_semicolon():
    header = '; length=123'
    assert was_modified_since(header, mtime=1, size=123) is True

def test_was_modified_since_header_starts_with_semicolon_size_mismatch():
    header = '; length=10'
    assert was_modified_since(header, mtime=1, size=0) is True

def test_was_modified_since_header_only_semicolon():
    header = ';;;'
    assert was_modified_since(header, mtime=1, size=0) is True

def test_was_modified_since_header_no_space_after_semicolon():
    header = ';length=10'
    assert was_modified_since(header, mtime=1, size=10) is True

def test_was_modified_since_header_non_digit_length():
    header = '; length=abc'
    assert was_modified_since(header, mtime=1, size=0) is True

def test_was_modified_since_header_semicolon_with_spaces_only():
    header = '; '
    assert was_modified_since(header, mtime=1, size=0) is True

def test_was_modified_since_valid_date_with_matching_length():
    mtime = 1600000000
    header = http_date(mtime) + '; length=42'
    assert was_modified_since(header, mtime, size=42) is False

def test_was_modified_since_valid_date_with_length_mismatch():
    mtime = 1600000000
    header = http_date(mtime) + '; length=43'
    assert was_modified_since(header, mtime, size=42) is True

def test_serve_with_malformed_if_modified_since_semicolon(client, media_dir):
    url = f'/site_media/file.txt'
    response = client.get(url, HTTP_IF_MODIFIED_SINCE='; length=123')
    assert response.status_code == 200
    with open(os.path.join(media_dir, 'file.txt'), 'rb') as fp:
        expected = fp.read()
    assert b''.join(response) == expected

def test_serve_with_malformed_if_modified_since_only_semicolon(client, media_dir):
    url = f'/site_media/file.txt'
    response = client.get(url, HTTP_IF_MODIFIED_SINCE=';')
    assert response.status_code == 200
    with open(os.path.join(media_dir, 'file.txt'), 'rb') as fp:
        expected = fp.read()
    assert b''.join(response) == expected

import unittest
from django.views.static import was_modified_since

class WasModifiedSinceMalformedHeaderTests(unittest.TestCase):
    """
    Ensure malformed or non-matching If-Modified-Since headers are treated
    as invalid/modified (i.e. was_modified_since(...) returns True) rather
    than raising exceptions. These inputs specifically exercise cases
    where the regex match can be None.
    """

    def test_semicolon_prefix_length(self):
        header = '; length=123'
        self.assertTrue(was_modified_since(header, mtime=1, size=123))

    def test_no_space_before_length_token(self):
        header = 'Wed, 20 Oct 2010 14:05:00 GMT;length=123'
        self.assertTrue(was_modified_since(header, mtime=1, size=123))

    def test_multiple_semicolons_before_length(self):
        header = 'Wed, 20 Oct 2010 14:05:00 GMT;; length=123'
        self.assertTrue(was_modified_since(header, mtime=1, size=123))

    def test_only_semicolon(self):
        header = ';'
        self.assertTrue(was_modified_since(header, mtime=1, size=0))

    def test_non_digit_length_value(self):
        header = 'Wed, 20 Oct 2010 14:05:00 GMT; length=12a3'
        self.assertTrue(was_modified_since(header, mtime=1, size=123))

    def test_empty_length_token(self):
        header = 'Wed, 20 Oct 2010 14:05:00 GMT; length='
        self.assertTrue(was_modified_since(header, mtime=1, size=0))

    def test_only_garbage_semicolons(self):
        header = ';;;;'
        self.assertTrue(was_modified_since(header, mtime=1, size=0))

    def test_semicolon_and_tab_before_length(self):
        header = 'Wed, 20 Oct 2010 14:05:00 GMT;\tlength=123'
        self.assertTrue(was_modified_since(header, mtime=1, size=123))

    def test_leading_semicolons_then_length(self):
        header = ';;; length=123'
        self.assertTrue(was_modified_since(header, mtime=1, size=123))

import unittest
from os import path
from django.test import SimpleTestCase
from django.views.static import was_modified_since
from django.utils.http import http_date
from .. import urls
from ..urls import media_dir

class WasModifiedSinceSemicolonTests(unittest.TestCase):

    def test_leading_semicolon_with_length_returns_true(self):
        header = '; length=123'
        self.assertTrue(was_modified_since(header=header, mtime=1, size=123))

    def test_leading_semicolon_without_length_returns_true(self):
        header = '; something'
        self.assertTrue(was_modified_since(header=header, mtime=1, size=0))

    def test_single_semicolon_returns_true(self):
        header = ';'
        self.assertTrue(was_modified_since(header=header, mtime=0, size=0))

    def test_multiple_semicolons_returns_true(self):
        header = ';;;'
        self.assertTrue(was_modified_since(header=header, mtime=0, size=0))

    def test_leading_semicolon_with_float_mtime_returns_true(self):
        header = '; length=0'
        mtime = 1343416141.107817
        self.assertTrue(was_modified_since(header=header, mtime=mtime, size=0))

import unittest
from os import path
from django.test import SimpleTestCase
from django.views.static import was_modified_since

class MoreStaticUtilsTests(unittest.TestCase):

    def test_was_modified_since_leading_semicolon_with_length(self):
        header = '; length=42'
        self.assertTrue(was_modified_since(header, mtime=1, size=42))

    def test_was_modified_since_leading_semicolon_length_mismatch(self):
        header = '; length=5'
        self.assertTrue(was_modified_since(header, mtime=1, size=10))

    def test_was_modified_since_leading_semicolon_no_length(self):
        header = '; no-date-or-length'
        self.assertTrue(was_modified_since(header, mtime=1, size=1))

    def test_was_modified_since_leading_semicolon_only_semicolon(self):
        header = ';'
        self.assertTrue(was_modified_since(header, mtime=1, size=0))

    def test_was_modified_since_leading_semicolon_with_date_like_text(self):
        header = '; Thu, 01 Jan 1970 00:00:00 GMT'
        self.assertTrue(was_modified_since(header, mtime=1, size=0))

from unittest.mock import patch
from unittest.mock import patch
import unittest
from django.utils.http import http_date
from django.views.static import was_modified_since

class WasModifiedSinceAttributeErrorTests(unittest.TestCase):

    def test_attribute_error_propagates_basic(self):
        header = http_date(1234567890)
        with patch('django.views.static.parse_http_date', side_effect=AttributeError('boom')):
            with self.assertRaises(AttributeError):
                was_modified_since(header, mtime=1234567890, size=0)

    def test_attribute_error_with_length_param(self):
        mtime = 1600000000
        size = 42
        header = f'{http_date(mtime)}; length={size}'
        with patch('django.views.static.parse_http_date', side_effect=AttributeError('boom')):
            with self.assertRaises(AttributeError):
                was_modified_since(header, mtime=mtime, size=size)

    def test_attribute_error_with_length_param_uppercase_keyword(self):
        mtime = 1600000001
        size = 7
        header = f'{http_date(mtime)}; LENGTH={size}'
        with patch('django.views.static.parse_http_date', side_effect=AttributeError('boom')):
            with self.assertRaises(AttributeError):
                was_modified_since(header, mtime=mtime, size=size)

    def test_attribute_error_with_space_before_semicolon(self):
        mtime = 1600000002
        size = 3
        header = f'{http_date(mtime)} ; length={size}'
        with patch('django.views.static.parse_http_date', side_effect=AttributeError('boom')):
            with self.assertRaises(AttributeError):
                was_modified_since(header, mtime=mtime, size=size)

    def test_attribute_error_with_trailing_spaces(self):
        mtime = 1600000003
        header = http_date(mtime) + '   '
        with patch('django.views.static.parse_http_date', side_effect=AttributeError('boom')):
            with self.assertRaises(AttributeError):
                was_modified_since(header, mtime=mtime, size=0)

    def test_attribute_error_with_unicode_in_header(self):
        mtime = 1600000004
        size = 1
        header = f'{http_date(mtime)}☃; length={size}'
        with patch('django.views.static.parse_http_date', side_effect=AttributeError('boom')):
            with self.assertRaises(AttributeError):
                was_modified_since(header, mtime=mtime, size=size)

    def test_attribute_error_with_multiple_spaces_and_tabs(self):
        mtime = 1600000005
        size = 5
        header = f'{http_date(mtime)} \t ; length={size}'
        with patch('django.views.static.parse_http_date', side_effect=AttributeError('boom')):
            with self.assertRaises(AttributeError):
                was_modified_since(header, mtime=mtime, size=size)

    def test_attribute_error_when_date_contains_comma_variations(self):
        mtime = 1600000007
        size = 4
        header = f'{http_date(mtime)}; length={size}'
        with patch('django.views.static.parse_http_date', side_effect=AttributeError('boom')):
            with self.assertRaises(AttributeError):
                was_modified_since(header, mtime=mtime, size=size)

    def test_attribute_error_with_long_timestamp_string(self):
        mtime = 1600000008
        size = 9
        long_prefix = 'X' * 50
        header = f'{http_date(mtime)}{long_prefix}; length={size}'
        with patch('django.views.static.parse_http_date', side_effect=AttributeError('boom')):
            with self.assertRaises(AttributeError):
                was_modified_since(header, mtime=mtime, size=size)

import unittest
from django.views.static import was_modified_since


class WasModifiedSinceMalformedHeaderTests(unittest.TestCase):
    """
    Regression tests for malformed If-Modified-Since header values that do not
    match the expected pattern. These inputs commonly start with a semicolon
    (e.g. a header containing only a length directive or malformed prefixes).
    The function should return True (treated as modified) and not raise.
    """

    def test_leading_semicolon_with_space(self):
        # Header starts with a semicolon followed by a length directive.
        header = "; length=123"
        self.assertTrue(was_modified_since(header, mtime=1, size=123))

    def test_leading_semicolon_without_space(self):
        # No space after semicolon (still malformed w.r.t. expected pattern).
        header = ";length=123"
        self.assertTrue(was_modified_since(header, mtime=1, size=123))

    def test_single_semicolon(self):
        header = ";"
        self.assertTrue(was_modified_since(header, mtime=1, size=0))

    def test_double_semicolon(self):
        header = ";; length=123"
        self.assertTrue(was_modified_since(header, mtime=1, size=123))

    def test_leading_semicolon_with_non_numeric_length(self):
        # Even if the length part contains non-digits, the leading semicolon
        # makes the whole header non-matching to the regex; should be treated
        # as modified (True) and not raise.
        header = "; length=abc"
        self.assertTrue(was_modified_since(header, mtime=1, size=0))

    def test_leading_semicolon_and_text(self):
        header = "; some unexpected text"
        self.assertTrue(was_modified_since(header, mtime=1, size=0))

    def test_semicolon_then_whitespace_only(self):
        header = "; "
        self.assertTrue(was_modified_since(header, mtime=1, size=0))

    def test_semicolon_then_multiple_spaces(self):
        header = ";    "
        self.assertTrue(was_modified_since(header, mtime=1, size=0))

    def test_semicolon_with_large_number(self):
        # Large numeric value after semicolon (still malformed because no date).
        header = "; length=99999999999999999999999"
        self.assertTrue(was_modified_since(header, mtime=1, size=0))

    def test_semicolon_and_equals_but_no_value(self):
        header = "; length="
        self.assertTrue(was_modified_since(header, mtime=1, size=0))

import unittest
from django.test import SimpleTestCase, override_settings
from django.views.static import was_modified_since
from os import path
from ..urls import media_dir

class MalformedHeaderWasModifiedTests(unittest.TestCase):
    """
    Unit tests for was_modified_since with malformed headers that do not match
    the expected regex. These headers often begin with a semicolon and should
    be treated as invalid, causing was_modified_since to return True.
    """

    def test_semicolon_only(self):
        self.assertTrue(was_modified_since(';', mtime=1, size=0))

    def test_semicolon_length(self):
        self.assertTrue(was_modified_since('; length=123', mtime=1, size=123))

    def test_semicolon_no_space(self):
        self.assertTrue(was_modified_since(';length=123', mtime=1, size=123))

    def test_double_semicolon(self):
        self.assertTrue(was_modified_since(';;', mtime=1, size=0))

    def test_semicolon_garbage(self):
        self.assertTrue(was_modified_since(';garbage', mtime=1, size=0))

    def test_semicolon_space_only(self):
        self.assertTrue(was_modified_since('; ', mtime=1, size=0))

@override_settings(DEBUG=True, ROOT_URLCONF='view_tests.urls')
class MalformedHeaderServeTests(SimpleTestCase):
    """
    Integration tests for the static file view to ensure malformed
    If-Modified-Since headers are handled gracefully and result in the
    full file being served (HTTP 200) rather than an internal server error.
    """
    prefix = 'site_media'

    def test_serve_handles_semicolon_only_header(self):
        self._assert_served_ok(';')

    def test_serve_handles_semicolon_length_header(self):
        self._assert_served_ok('; length=123')

    def test_serve_handles_semicolon_no_space_header(self):
        self._assert_served_ok(';length=123')

    def test_serve_handles_double_semicolon_header(self):
        self._assert_served_ok(';;')

from django.test import SimpleTestCase
from django.views.static import was_modified_since
from django.utils.http import http_date

class WasModifiedSinceAdditionalTests(SimpleTestCase):

    def test_semicolon_with_non_numeric_length(self):
        header = 'Wed, 21 Oct 2015 07:28:00 GMT; length=abc'
        self.assertTrue(was_modified_since(header, mtime=1, size=1))

    def test_trailing_semicolon_only(self):
        header = f'{http_date(100)};'
        self.assertTrue(was_modified_since(header, mtime=100, size=10))

import unittest
from django.views.static import was_modified_since


class WasModifiedSinceSemicolonHeaderRegressionTests(unittest.TestCase):
    """
    Regression tests for headers that start with a semicolon. These headers make
    the regex match return None. The fixed implementation detects this and
    treats the header as invalid (returning True). The faulty model patch
    accesses groups on a None match and raises a TypeError.
    """

    def test_semicolon_length_header(self):
        header = "; length=123"
        self.assertTrue(was_modified_since(header, mtime=0, size=123))

    def test_semicolon_only_header(self):
        header = ";"
        self.assertTrue(was_modified_since(header, mtime=0, size=0))

    def test_semicolon_with_space_header(self):
        header = "; "
        self.assertTrue(was_modified_since(header, mtime=1, size=0))

    def test_semicolon_with_non_numeric_length(self):
        header = "; length=abc"
        self.assertTrue(was_modified_since(header, mtime=0, size=0))

    def test_semicolon_with_trailing_text(self):
        header = "; length=123 extra"
        self.assertTrue(was_modified_since(header, mtime=0, size=123))

    def test_double_semicolon_header(self):
        header = ";; length=123"
        self.assertTrue(was_modified_since(header, mtime=0, size=123))

    def test_semicolon_length_mismatch(self):
        header = "; length=5"
        # size doesn't match header length -> invalid header -> True
        self.assertTrue(was_modified_since(header, mtime=0, size=10))

    def test_semicolon_with_date_like_text(self):
        header = "; Wed, 21 Oct 2015 07:28:00 GMT"
        self.assertTrue(was_modified_since(header, mtime=0, size=0))

    def test_semicolon_zero_length(self):
        header = "; length=0"
        self.assertTrue(was_modified_since(header, mtime=0, size=0))

    def test_semicolon_with_mtime_nonzero(self):
        header = "; length=456"
        self.assertTrue(was_modified_since(header, mtime=1000, size=456))

from os import path

from django.test import SimpleTestCase, override_settings

from django.views.static import was_modified_since

from ..urls import media_dir

@override_settings(DEBUG=True, ROOT_URLCONF="view_tests.urls")
class SemicolonHeaderRegressionTests(SimpleTestCase):
    """
    Regression tests to ensure headers that start with ';' (and thus don't
    match the expected regex) are handled without raising exceptions.
    """

    prefix = "site_media"
    sample_file = "file.txt"

    # Direct tests for was_modified_since with various leading-semicolon headers

    def test_was_modified_since_semicolon_only(self):
        self.assertTrue(was_modified_since(";", mtime=1, size=1))

    def test_was_modified_since_leading_semicolon_with_length(self):
        self.assertTrue(was_modified_since("; length=123", mtime=1, size=123))

    def test_was_modified_since_leading_semicolon_garbage(self):
        self.assertTrue(was_modified_since("; some random text", mtime=1, size=0))

    def test_was_modified_since_leading_semicolon_no_space_before_length(self):
        # ";length=1" doesn't match "; length=([0-9]+)" so re.match returns None.
        self.assertTrue(was_modified_since(";length=1", mtime=1, size=1))

    def test_was_modified_since_leading_semicolon_unexpected_key(self):
        self.assertTrue(was_modified_since("; something=else", mtime=1, size=0))

    def test_was_modified_since_leading_semicolon_and_size_zero(self):
        self.assertTrue(was_modified_since("; length=0", mtime=0, size=0))

    # Integration tests using the test client to ensure the view doesn't error

    def test_serve_handles_leading_semicolon_length(self):
        response = self.client.get(
            "/%s/%s" % (self.prefix, self.sample_file),
            HTTP_IF_MODIFIED_SINCE="; length=123",
        )
        # Should return the content (200) and not raise
        self.assertEqual(response.status_code, 200)
        with open(path.join(media_dir, self.sample_file), "rb") as fp:
            self.assertEqual(fp.read(), b"".join(response))

    def test_serve_handles_semicolon_only_header(self):
        response = self.client.get(
            "/%s/%s" % (self.prefix, self.sample_file), HTTP_IF_MODIFIED_SINCE=";"
        )
        self.assertEqual(response.status_code, 200)
        with open(path.join(media_dir, self.sample_file), "rb") as fp:
            self.assertEqual(fp.read(), b"".join(response))

    def test_serve_handles_semicolon_and_date(self):
        response = self.client.get(
            "/%s/%s" % (self.prefix, self.sample_file),
            HTTP_IF_MODIFIED_SINCE="; Mon, 01 Jan 2001 00:00:00 GMT",
        )
        self.assertEqual(response.status_code, 200)
        with open(path.join(media_dir, self.sample_file), "rb") as fp:
            self.assertEqual(fp.read(), b"".join(response))

    def test_serve_handles_leading_semicolon_no_space_length(self):
        # Header ";length=1" is malformed for the regex and should be treated as invalid
        response = self.client.get(
            "/%s/%s" % (self.prefix, self.sample_file),
            HTTP_IF_MODIFIED_SINCE=";length=1",
        )
        self.assertEqual(response.status_code, 200)
        with open(path.join(media_dir, self.sample_file), "rb") as fp:
            self.assertEqual(fp.read(), b"".join(response))

from os import path
from django.test import SimpleTestCase, override_settings
from os import path
import unittest

from django.test import SimpleTestCase, override_settings
from django.views.static import was_modified_since
from django.test import override_settings

# media_dir and URL configuration are provided by the existing test package.
from .. import urls
from ..urls import media_dir


@override_settings(DEBUG=True, ROOT_URLCONF="view_tests.urls")
class WasModifiedSinceSemicolonTests(SimpleTestCase):
    """
    Regression tests for was_modified_since when the header begins with a semicolon.

    These headers do not match the regex r"^([^;]+)(; length=([0-9]+))?$" because
    they start with a semicolon. The fixed implementation detects a non-match and
    treats the header as invalid (return True). The candidate model patch fails
    to detect the non-match and will raise an exception.
    """

    def test_leading_semicolon_length_numeric(self):
        header = "; length=123"
        self.assertTrue(was_modified_since(header, mtime=1, size=0))

    def test_leading_semicolon_length_no_space(self):
        header = ";length=123"
        self.assertTrue(was_modified_since(header, mtime=1, size=0))

    def test_leading_semicolon_only_semicolon(self):
        header = ";"
        self.assertTrue(was_modified_since(header, mtime=1, size=0))

    def test_leading_semicolon_with_garbage(self):
        header = "; some garbage text"
        self.assertTrue(was_modified_since(header, mtime=1, size=0))

    def test_leading_semicolon_with_date_and_length(self):
        header = "; Fri, 01 Jan 1990 00:00:00 GMT; length=5"
        self.assertTrue(was_modified_since(header, mtime=1, size=0))

    def test_leading_semicolon_length_non_numeric(self):
        header = ";length=abc"
        self.assertTrue(was_modified_since(header, mtime=1, size=0))

    def test_leading_semicolon_multiple_semicolons(self):
        header = ";; length=5"
        self.assertTrue(was_modified_since(header, mtime=1, size=0))

    def test_leading_semicolon_trailing_attrs(self):
        header = "; length=5; another=1"
        self.assertTrue(was_modified_since(header, mtime=1, size=0))

    # Integration-style checks using the test client to ensure the view handles such headers.
    def test_serve_with_leading_semicolon_length_header(self):
        filename = "file.txt"
        header = "; length=123"
        response = self.client.get("/site_media/%s" % filename, HTTP_IF_MODIFIED_SINCE=header)
        # Should serve the file (200) rather than crash.
        self.assertEqual(response.status_code, 200)
        response_content = b"".join(response)
        with open(path.join(media_dir, filename), "rb") as fp:
            self.assertEqual(fp.read(), response_content)

    def test_serve_with_leading_semicolon_only(self):
        filename = "file.txt"
        header = ";"
        response = self.client.get("/site_media/%s" % filename, HTTP_IF_MODIFIED_SINCE=header)
        self.assertEqual(response.status_code, 200)
        response_content = b"".join(response)
        with open(path.join(media_dir, filename), "rb") as fp:
            self.assertEqual(fp.read(), response_content)

from unittest.mock import patch

from django.test import SimpleTestCase
from django.utils.http import http_date
from django.views.static import was_modified_since

class WasModifiedSinceAttributeErrorTests(SimpleTestCase):
    """
    Regression tests to ensure AttributeError from parse_http_date is not
    silently caught by was_modified_since.
    """

    @patch("django.views.static.parse_http_date", side_effect=AttributeError("boom"))
    def test_attribute_error_propagates_basic(self, mock_parse):
        header = http_date(1234567890)
        with self.assertRaises(AttributeError):
            was_modified_since(header, mtime=1234567890, size=0)

    @patch("django.views.static.parse_http_date", side_effect=AttributeError("boom"))
    def test_attribute_error_propagates_with_length(self, mock_parse):
        header = f"{http_date(0)}; length=5"
        with self.assertRaises(AttributeError):
            was_modified_since(header, mtime=0, size=5)

    @patch("django.views.static.parse_http_date", side_effect=AttributeError("boom"))
    def test_attribute_error_propagates_length_zero(self, mock_parse):
        header = f"{http_date(0)}; length=0"
        with self.assertRaises(AttributeError):
            was_modified_since(header, mtime=0, size=0)

    @patch("django.views.static.parse_http_date", side_effect=AttributeError("boom"))
    def test_attribute_error_propagates_case_insensitive_length(self, mock_parse):
        header = f"{http_date(0)}; LeNgTh=7"
        with self.assertRaises(AttributeError):
            was_modified_since(header, mtime=0, size=7)

    @patch("django.views.static.parse_http_date", side_effect=AttributeError("boom"))
    def test_attribute_error_propagates_with_trailing_space_before_semicolon(self, mock_parse):
        # group1 will include the trailing space, but parse_http_date is still called
        header = http_date(0) + " ; length=3"
        with self.assertRaises(AttributeError):
            was_modified_since(header, mtime=0, size=3)

    @patch("django.views.static.parse_http_date", side_effect=AttributeError("boom"))
    def test_attribute_error_propagates_large_mtime(self, mock_parse):
        header = http_date(2000000000)
        with self.assertRaises(AttributeError):
            was_modified_since(header, mtime=2000000000, size=1)

    @patch("django.views.static.parse_http_date", side_effect=AttributeError("boom"))
    def test_attribute_error_propagates_unicode_header(self, mock_parse):
        # http_date contains commas and spaces; still should call parse_http_date
        header = http_date(987654321)
        with self.assertRaises(AttributeError):
            was_modified_since(header, mtime=987654321, size=2)

    @patch("django.views.static.parse_http_date", side_effect=AttributeError("boom"))
    def test_attribute_error_propagates_long_length(self, mock_parse):
        header = f"{http_date(0)}; length=999999"
        with self.assertRaises(AttributeError):
            was_modified_since(header, mtime=0, size=999999)

    @patch("django.views.static.parse_http_date", side_effect=AttributeError("boom"))
    def test_attribute_error_propagates_matching_mtime_smaller(self, mock_parse):
        # Even if mtime < header_mtime (would normally return True), parse_http_date
        # is invoked first and should raise the AttributeError
        header = http_date(1000000)
        with self.assertRaises(AttributeError):
            was_modified_since(header, mtime=1, size=0)

    @patch("django.views.static.parse_http_date", side_effect=AttributeError("boom"))
    def test_attribute_error_propagates_matching_mtime_greater(self, mock_parse):
        # Even if mtime > header_mtime (would normally raise ValueError later),
        # parse_http_date is still called first and should raise the AttributeError
        header = http_date(1000)
        with self.assertRaises(AttributeError):
            was_modified_since(header, mtime=2000, size=0)

import unittest
from django.views.static import was_modified_since

class WasModifiedSinceInvalidHeaderTests(unittest.TestCase):

    def test_leading_semicolon_with_length(self):
        self.assertTrue(was_modified_since('; length=123', mtime=1, size=0))

    def test_non_digit_length_value(self):
        header = 'Wed, 21 Oct 2015 07:28:00 GMT; length=abc'
        self.assertTrue(was_modified_since(header, mtime=1, size=0))

    def test_trailing_semicolon_only(self):
        header = 'Wed, 21 Oct 2015 07:28:00 GMT;'
        self.assertTrue(was_modified_since(header, mtime=1, size=0))

    def test_arbitrary_semicolon_pairs(self):
        self.assertTrue(was_modified_since('foo;bar', mtime=1, size=0))

    def test_empty_length_assignment(self):
        self.assertTrue(was_modified_since('GMT; length=', mtime=1, size=0))

    def test_negative_length_value(self):
        self.assertTrue(was_modified_since('foo; length=-5', mtime=1, size=0))

    def test_unrecognized_parameter_after_date(self):
        header = 'Thu, 1 Jan 1970 00:00:00 GMT; something=123'
        self.assertTrue(was_modified_since(header, mtime=1, size=0))

    def test_no_space_after_semicolon_length(self):
        self.assertTrue(was_modified_since(';length=5', mtime=1, size=0))