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