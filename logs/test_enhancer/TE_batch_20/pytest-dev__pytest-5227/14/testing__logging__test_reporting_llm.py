import re
import os
import logging
import pytest
LOG_LINE_RE = re.compile('(DEBUG|INFO|WARNING|ERROR|CRITICAL)\\s+\\S+:\\S+\\.py:\\d+\\s+(.+)')