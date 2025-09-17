import types
import pytest
from _pytest.skipping import pytest_runtest_makereport, skipped_by_mark_key, xfailed_key, unexpectedsuccess_key
from _pytest.outcomes import xfail as xfail_module