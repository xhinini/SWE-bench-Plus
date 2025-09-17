import re
import queue
import types
from requests.exceptions import HTTPError, TooManyRedirects
import pytest
import json
from sphinx.builders.linkcheck import CheckExternalLinksBuilder
import sphinx.builders.linkcheck as linkcheck_module
from types import SimpleNamespace