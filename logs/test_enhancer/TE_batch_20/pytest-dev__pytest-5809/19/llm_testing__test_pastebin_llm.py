from __future__ import absolute_import, division, print_function
import sys
import pytest
if sys.version_info < (3, 0):
    import urlparse as _parse
    parse_qs = _parse.parse_qs
else:
    import urllib.parse as _parse
    parse_qs = _parse.parse_qs