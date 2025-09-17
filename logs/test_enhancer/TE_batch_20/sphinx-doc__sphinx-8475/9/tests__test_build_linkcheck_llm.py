import http.server
import json
import socket
from types import SimpleNamespace
import pytest
from requests.exceptions import HTTPError, TooManyRedirects
from pathlib import Path
from sphinx.util import logging