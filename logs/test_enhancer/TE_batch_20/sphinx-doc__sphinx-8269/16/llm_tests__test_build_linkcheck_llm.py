from docutils import nodes
from requests.exceptions import HTTPError
from sphinx.builders.linkcheck import CheckExternalLinksBuilder
import time
import io
import threading
from unittest import mock
import pytest
from docutils import nodes
from requests.exceptions import HTTPError
from sphinx.builders import linkcheck as linkcheck_mod