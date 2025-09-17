from _pytest.unittest import TestCaseFunction, UnitTestCase
import _pytest.debugging
import types
import pytest
from _pytest.unittest import TestCaseFunction, UnitTestCase
import _pytest.debugging
pytest.fixture(autouse=True)(lambda monkeypatch: monkeypatch.setattr(_pytest.debugging, 'maybe_wrap_pytest_function_for_tracing', lambda x: None))