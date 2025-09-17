import logging
import os
import pytest
import six
from _pytest import logging as _logging
from _pytest.logging import DEFAULT_LOG_FORMAT, ColoredLevelFormatter, catching_logs, LogCaptureHandler, LogCaptureFixture, get_actual_log_level
from _pytest.logging import _LiveLoggingStreamHandler