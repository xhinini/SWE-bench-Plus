import logging
import types
import pytest
import py
import six
from _pytest import logging as pytest_logging
from _pytest.logging import ColoredLevelFormatter, DEFAULT_LOG_FORMAT, LEVELNAME_FMT_REGEX
from _pytest.logging import get_actual_log_level, catching_logs, LogCaptureHandler, LogCaptureFixture