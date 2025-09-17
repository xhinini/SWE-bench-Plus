import mock
from requests.exceptions import HTTPError
import os
import tempfile
from pathlib import Path
from unittest import mock
import threading
import queue
import time
import pytest
from requests.exceptions import HTTPError
from sphinx.builders.linkcheck import CheckExternalLinksBuilder