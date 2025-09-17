import os
import shutil
import tempfile
from django import conf
from django.test import SimpleTestCase
from django.test.utils import extend_sys_path

def _parse_headers(response):
    """
    Parse response.serialize_headers() into a dict of header -> value.
    """
    headers = {}
    for line in response.serialize_headers().split(b'\r\n'):
        if not line:
            continue
        try:
            name, value = line.split(b': ', 1)
        except ValueError:
            continue
        headers[name.decode('ascii')] = value.decode('ascii')
    return headers