from docutils import nodes
from unittest import mock
import pytest
from urllib.parse import unquote
from sphinx.builders import linkcheck as linkcheck_mod
from requests.exceptions import HTTPError