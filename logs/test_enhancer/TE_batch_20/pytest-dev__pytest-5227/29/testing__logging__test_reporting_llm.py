import logging
import contextlib
import pytest
from functools import partial
from _pytest.logging import ColoredLevelFormatter, get_actual_log_level, catching_logs, LogCaptureHandler, LogCaptureFixture