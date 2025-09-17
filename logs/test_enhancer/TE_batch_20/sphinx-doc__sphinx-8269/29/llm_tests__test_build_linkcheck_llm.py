import os
import queue
import tempfile
from unittest import mock
import pytest
from sphinx.builders.linkcheck import CheckExternalLinksBuilder
from types import SimpleNamespace