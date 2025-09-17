import logging
import os
import io
from types import SimpleNamespace
import py
import pytest
import six
import logging
import os
import io
import contextlib
from types import SimpleNamespace
import py
import pytest
import six
from _pytest import logging as _logging
from _pytest.logging import ColoredLevelFormatter, catching_logs, LogCaptureHandler, LogCaptureFixture, LoggingPlugin, DEFAULT_LOG_FORMAT, DEFAULT_LOG_DATE_FORMAT