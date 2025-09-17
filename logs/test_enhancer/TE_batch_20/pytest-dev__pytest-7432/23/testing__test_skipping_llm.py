from types import SimpleNamespace
import attr
from _pytest.outcomes import xfail as _xfail
from _pytest.skipping import skipped_by_mark_key, xfailed_key
from _pytest.store import StoreKey
import types
import attr
import pytest
from types import SimpleNamespace
from _pytest.skipping import pytest_runtest_makereport, skipped_by_mark_key, xfailed_key
from _pytest.outcomes import xfail as _xfail
from _pytest.store import StoreKey