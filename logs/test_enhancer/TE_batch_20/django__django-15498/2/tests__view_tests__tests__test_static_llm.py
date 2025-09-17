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