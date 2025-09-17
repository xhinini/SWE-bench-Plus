import types
from _pytest.outcomes import xfail as _xfail
from _pytest.skipping import pytest_runtest_makereport, skipped_by_mark_key, xfailed_key
from _pytest.skipping import Xfail