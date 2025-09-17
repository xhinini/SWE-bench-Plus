import re
import re
import pytest
from _pytest.pytester import Pytester
ansi_re = re.compile('\\x1b\\[[0-9;]*m')