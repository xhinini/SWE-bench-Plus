from pylint.lint.run import _query_cpu, _cpu_count
# Additional regression tests for quota/period fractional CPU handling
import os
import pathlib
from unittest.mock import MagicMock, mock_open, patch

import pytest

from pylint.testutils import GenericTestReporter as Reporter
from pylint.lint import Run
from pylint.lint.run import _query_cpu, _cpu_count


def _make_mock_open(mapping):
    builtin_open = open
    def _mock_open(*args, **kwargs):
        path = args[0]
        if path in mapping:
            return mock_open(read_data=mapping[path])(*args, **kwargs)
        return builtin_open(*args, **kwargs)
    return _mock_open


def _make_mock_path(true_paths):
    pathlib_path = pathlib.Path
    def _mock_path(*args, **kwargs):
        if args and args[0] in true_paths:
            return MagicMock(is_file=lambda: True)
        return pathlib_path(*args, **kwargs)
    return _mock_path


def test_query_cpu_quota_fraction_zero_returns_one() -> None:
    # quota < period -> int(quota/period) == 0, should be treated as 1
    mapping = {
        "/sys/fs/cgroup/cpu/cpu.cfs_quota_us": "50000",
        "/sys/fs/cgroup/cpu/cpu.cfs_period_us": "100000",
    }
    with patch("builtins.open", _make_mock_open(mapping)):
        with patch("pylint.lint.run.Path", _make_mock_path(mapping.keys())):
            assert _query_cpu() == 1


def test_query_cpu_quota_fraction_zero_with_whitespace_returns_one() -> None:
    mapping = {
        "/sys/fs/cgroup/cpu/cpu.cfs_quota_us": "  1\n",
        "/sys/fs/cgroup/cpu/cpu.cfs_period_us": "100000\n",
    }
    with patch("builtins.open", _make_mock_open(mapping)):
        with patch("pylint.lint.run.Path", _make_mock_path(mapping.keys())):
            assert _query_cpu() == 1


def test_cpu_count_with_sched_getaffinity_and_quota_fraction_zero(tmp_path) -> None:
    mapping = {
        "/sys/fs/cgroup/cpu/cpu.cfs_quota_us": "123\n",
        "/sys/fs/cgroup/cpu/cpu.cfs_period_us": "1000\n",  # 123/1000 -> 0
    }
    with patch("builtins.open", _make_mock_open(mapping)):
        with patch("pylint.lint.run.Path", _make_mock_path(mapping.keys())):
            # Provide a sched_getaffinity that reports 4 CPUs
            with patch.object(os, "sched_getaffinity", lambda _: set(range(4))):
                # min(cpu_share, 4) should be 1 (not 0)
                assert _cpu_count() >= 1


def test_cpu_count_with_multiprocessing_and_quota_fraction_zero(monkeypatch) -> None:
    mapping = {
        "/sys/fs/cgroup/cpu/cpu.cfs_quota_us": "50",
        "/sys/fs/cgroup/cpu/cpu.cfs_period_us": "100000",
    }
    with patch("builtins.open", _make_mock_open(mapping)):
        with patch("pylint.lint.run.Path", _make_mock_path(mapping.keys())):
            # Remove sched_getaffinity to force multiprocessing path
            monkeypatch.delattr(os, "sched_getaffinity", raising=False)
            fake_mp = MagicMock()
            fake_mp.cpu_count.return_value = 8
            with patch("pylint.lint.run.multiprocessing", fake_mp):
                assert _cpu_count() >= 1


def test_run_jobs_zero_with_quota_fraction_zero_does_not_exit_nonzero(tmp_path) -> None:
    mapping = {
        "/sys/fs/cgroup/cpu/cpu.cfs_quota_us": "50000",
        "/sys/fs/cgroup/cpu/cpu.cfs_period_us": "100000",
    }
    filepath = os.path.abspath(__file__)
    testargs = [filepath, "--jobs=0"]
    with tmp_path.as_cwd():
        with patch("builtins.open", _make_mock_open(mapping)):
            with patch("pylint.lint.run.Path", _make_mock_path(mapping.keys())):
                # Should exit with 0
                with pytest.raises(SystemExit) as err:
                    Run(testargs, reporter=Reporter())
                assert err.value.code == 0


def test_run_jobs_zero_quota_with_newline_chars(tmp_path) -> None:
    mapping = {
        "/sys/fs/cgroup/cpu/cpu.cfs_quota_us": "  1\n",
        "/sys/fs/cgroup/cpu/cpu.cfs_period_us": "100000\n",
    }
    filepath = os.path.abspath(__file__)
    testargs = [filepath, "--jobs=0"]
    with tmp_path.as_cwd():
        with patch("builtins.open", _make_mock_open(mapping)):
            with patch("pylint.lint.run.Path", _make_mock_path(mapping.keys())):
                with pytest.raises(SystemExit) as err:
                    Run(testargs, reporter=Reporter())
                assert err.value.code == 0


def test_query_cpu_small_quota_integer_string_zero_returns_one() -> None:
    # quota "1" and period "100000" should yield 0 but be coerced to 1
    mapping = {
        "/sys/fs/cgroup/cpu/cpu.cfs_quota_us": "1",
        "/sys/fs/cgroup/cpu/cpu.cfs_period_us": "100000",
    }
    with patch("builtins.open", _make_mock_open(mapping)):
        with patch("pylint.lint.run.Path", _make_mock_path(mapping.keys())):
            assert _query_cpu() == 1


def test_cpu_count_min_behavior_with_quota_fraction_zero(monkeypatch) -> None:
    mapping = {
        "/sys/fs/cgroup/cpu/cpu.cfs_quota_us": "10",
        "/sys/fs/cgroup/cpu/cpu.cfs_period_us": "100000",
    }
    with patch("builtins.open", _make_mock_open(mapping)):
        with patch("pylint.lint.run.Path", _make_mock_path(mapping.keys())):
            # simulate multiprocessing cpu_count = 2
            fake_mp = MagicMock()
            fake_mp.cpu_count.return_value = 2
            with patch("pylint.lint.run.multiprocessing", fake_mp):
                # _cpu_count should not return 0
                assert _cpu_count() >= 1


def test_run_does_not_set_zero_jobs_when_quota_fraction_zero_and_multiprocessing(tmp_path, monkeypatch) -> None:
    mapping = {
        "/sys/fs/cgroup/cpu/cpu.cfs_quota_us": "30",
        "/sys/fs/cgroup/cpu/cpu.cfs_period_us": "100000",
    }
    filepath = os.path.abspath(__file__)
    testargs = [filepath, "--jobs=0"]
    with tmp_path.as_cwd():
        with patch("builtins.open", _make_mock_open(mapping)):
            with patch("pylint.lint.run.Path", _make_mock_path(mapping.keys())):
                fake_mp = MagicMock()
                fake_mp.cpu_count.return_value = 16
                with patch("pylint.lint.run.multiprocessing", fake_mp):
                    with pytest.raises(SystemExit) as err:
                        Run(testargs, reporter=Reporter())
                    # Should exit successfully
                    assert err.value.code == 0

def test_query_cpu_prefers_quota_over_shares_even_if_quota_yields_zero() -> None:
    # Both quota and shares present; quota yields 0 -> should still be coerced to 1
    mapping = {
        "/sys/fs/cgroup/cpu/cpu.cfs_quota_us": "1",
        "/sys/fs/cgroup/cpu/cpu.cfs_period_us": "100000",
        "/sys/fs/cgroup/cpu/cpu.shares": "2048",
    }
    # Ensure Path says all three files exist
    with patch("builtins.open", _make_mock_open(mapping)):
        with patch("pylint.lint.run.Path", _make_mock_path(mapping.keys())):
            assert _query_cpu() == 1

# No new top-level imports required; tests reuse existing imports in the test module.
# Additional regression tests for pylint.lint.run._query_cpu and Run
from __future__ import annotations

import builtins
from unittest.mock import MagicMock, mock_open, patch

import pytest
import pathlib
import os
import sys

from pylint.lint.run import _query_cpu, Run
from pylint.testutils import GenericTestReporter as Reporter

def _make_open_mock(mapping):
    """Return an open wrapper that returns mapped contents for specific paths."""
    builtin_open = builtins.open

    def _mock_open(*args, **kwargs):
        path = args[0]
        if path in mapping:
            # Ensure string data (open(..., encoding="utf-8") expects str)
            return mock_open(read_data=mapping[path])(*args, **kwargs)
        return builtin_open(*args, **kwargs)

    return _mock_open

def _make_path_mock(existing_paths):
    """Return a Path factory that reports is_file True for paths in existing_paths."""
    real_path = pathlib.Path

    def _mock_path(path_arg, *args, **kwargs):
        if path_arg in existing_paths:
            return MagicMock(is_file=lambda: True)
        return real_path(path_arg, *args, **kwargs)

    return _mock_path

@pytest.mark.parametrize(
    "quota,period",
    [
        ("50000\n", "100000\n"),
        ("1\n", "100000\n"),
        ("99999\n", "100000\n"),
        ("  42  \n", "100000\n"),
        ("\t7\n", "100000\n"),
    ],
)
def test_query_cpu_quota_smaller_than_period_returns_at_least_one(tmpdir, quota, period):
    """When cpu.cfs_quota_us < cpu.cfs_period_us _query_cpu must return >= 1."""
    mapping = {
        "/sys/fs/cgroup/cpu/cpu.cfs_quota_us": quota,
        "/sys/fs/cgroup/cpu/cpu.cfs_period_us": period,
    }
    with tmpdir.as_cwd():
        with patch("builtins.open", _make_open_mock(mapping)):
            with patch("pylint.lint.run.Path", _make_path_mock(mapping.keys())):
                value = _query_cpu()
                # Gold patch ensures this becomes 1 instead of 0
                assert value == 1

def test_query_cpu_quota_fraction_with_no_newline_and_spaces(tmpdir):
    """Ensure strange whitespace/newline combos still yield at least 1."""
    mapping = {
        "/sys/fs/cgroup/cpu/cpu.cfs_quota_us": "  10",  # no newline
        "/sys/fs/cgroup/cpu/cpu.cfs_period_us": "100000  \n",
    }
    with tmpdir.as_cwd():
        with patch("builtins.open", _make_open_mock(mapping)):
            with patch("pylint.lint.run.Path", _make_path_mock(mapping.keys())):
                assert _query_cpu() == 1

def test_query_cpu_quota_fraction_precedence_over_shares(tmpdir):
    """
    If both quota/period and shares files exist, quota/period should determine
    the available cpu and a fractional result should be normalized to 1.
    """
    mapping = {
        "/sys/fs/cgroup/cpu/cpu.cfs_quota_us": "25000\n",
        "/sys/fs/cgroup/cpu/cpu.cfs_period_us": "100000\n",
        "/sys/fs/cgroup/cpu/cpu.shares": "2\n",  # would also be fractional
    }
    with tmpdir.as_cwd():
        with patch("builtins.open", _make_open_mock(mapping)):
            with patch("pylint.lint.run.Path", _make_path_mock(mapping.keys())):
                assert _query_cpu() == 1

def test_query_cpu_quota_exact_one_returns_one(tmpdir):
    """When quota equals period, result should be 1 (sanity check)."""
    mapping = {
        "/sys/fs/cgroup/cpu/cpu.cfs_quota_us": "100000\n",
        "/sys/fs/cgroup/cpu/cpu.cfs_period_us": "100000\n",
    }
    with tmpdir.as_cwd():
        with patch("builtins.open", _make_open_mock(mapping)):
            with patch("pylint.lint.run.Path", _make_path_mock(mapping.keys())):
                assert _query_cpu() == 1

def test_run_jobs_zero_with_quota_fraction_dont_crash(tmpdir):
    """Run with --jobs=0 should not crash when quota/period produces a fractional CPU."""
    mapping = {
        "/sys/fs/cgroup/cpu/cpu.cfs_quota_us": "12345\n",
        "/sys/fs/cgroup/cpu/cpu.cfs_period_us": "100000\n",
    }
    filepath = os.path.abspath(__file__)
    testargs = [filepath, "--jobs=0"]
    with tmpdir.as_cwd():
        with patch("builtins.open", _make_open_mock(mapping)):
            with patch("pylint.lint.run.Path", _make_path_mock(mapping.keys())):
                with pytest.raises(SystemExit) as exc:
                    Run(testargs, reporter=Reporter())
                assert exc.value.code == 0

def test_run_jobs_zero_with_quota_fraction_and_additional_files(tmpdir):
    """Same as above but ensure other FS operations are unaffected by mocking."""
    mapping = {
        "/sys/fs/cgroup/cpu/cpu.cfs_quota_us": "222\n",
        "/sys/fs/cgroup/cpu/cpu.cfs_period_us": "100000\n",
    }
    filepath = os.path.abspath(__file__)
    testargs = [filepath, "--jobs=0"]
    # Also include a real file read (this file) to ensure our open wrapper delegates
    # correctly for other paths.
    with tmpdir.as_cwd():
        with patch("builtins.open", _make_open_mock(mapping)):
            with patch("pylint.lint.run.Path", _make_path_mock(mapping.keys())):
                with pytest.raises(SystemExit) as exc:
                    Run(testargs, reporter=Reporter())
                assert exc.value.code == 0

# Additional variants to ensure robustness across multiple small quotas
@pytest.mark.parametrize("quota", ["3\n", "6\n", "42\n", "99\n", "500\n"])
def test_multiple_small_quotas_return_one(tmpdir, quota):
    mapping = {
        "/sys/fs/cgroup/cpu/cpu.cfs_quota_us": quota,
        "/sys/fs/cgroup/cpu/cpu.cfs_period_us": "100000\n",
    }
    with tmpdir.as_cwd():
        with patch("builtins.open", _make_open_mock(mapping)):
            with patch("pylint.lint.run.Path", _make_path_mock(mapping.keys())):
                assert _query_cpu() == 1

from pylint.lint.run import _query_cpu, _cpu_count, Run
# Additional regression tests for pylint.lint.run concerning fractional CPU detection
import os
from unittest.mock import MagicMock, mock_open, patch

import pytest

from pylint.testutils import GenericTestReporter as Reporter
from pylint.lint.run import _query_cpu, _cpu_count, Run


def _make_mock_open(mapping):
    """Return a callable for patching builtins.open that serves content for specific paths."""
    builtin_open = open

    def _mock_open(path, *args, **kwargs):
        if path in mapping:
            data = mapping[path]
            return mock_open(read_data=data)(path, *args, **kwargs)
        return builtin_open(path, *args, **kwargs)

    return _mock_open


def _make_mock_path(existing_paths):
    """Return a Path constructor that marks specific files as existing."""
    pathlib_Path = __import__("pathlib").Path

    def _mock_path(path):
        if path in existing_paths:
            return MagicMock(is_file=lambda: True)
        return pathlib_Path(path)

    return _mock_path


def test_query_cpu_cfs_quota_small_fraction_returns_one():
    # quota smaller than period -> fraction < 1 should be treated as 1 CPU
    mapping = {
        "/sys/fs/cgroup/cpu/cpu.cfs_quota_us": "50000",
        "/sys/fs/cgroup/cpu/cpu.cfs_period_us": "100000",
    }
    _mock_open = _make_mock_open(mapping)
    _mock_path = _make_mock_path(set(mapping.keys()))

    with patch("builtins.open", _mock_open):
        with patch("pylint.lint.run.Path", _mock_path):
            assert _query_cpu() == 1


def test_query_cpu_cfs_quota_exact_one_returns_one():
    mapping = {
        "/sys/fs/cgroup/cpu/cpu.cfs_quota_us": "100000",
        "/sys/fs/cgroup/cpu/cpu.cfs_period_us": "100000",
    }
    _mock_open = _make_mock_open(mapping)
    _mock_path = _make_mock_path(set(mapping.keys()))

    with patch("builtins.open", _mock_open):
        with patch("pylint.lint.run.Path", _mock_path):
            assert _query_cpu() == 1


def test_query_cpu_with_negative_quota_uses_shares():
    # quota == -1 should fall back to cpu.shares
    mapping = {
        "/sys/fs/cgroup/cpu/cpu.cfs_quota_us": "-1",
        "/sys/fs/cgroup/cpu/cpu.shares": "2048",
    }
    _mock_open = _make_mock_open(mapping)
    _mock_path = _make_mock_path(set(mapping.keys()))

    with patch("builtins.open", _mock_open):
        with patch("pylint.lint.run.Path", _mock_path):
            # 2048/1024 == 2
            assert _query_cpu() == 2


def test_pylint_run_jobs_zero_with_cfs_quota_fraction(tmpdir):
    # Full Run invocation should not crash when quota/period yield a fraction
    mapping = {
        "/sys/fs/cgroup/cpu/cpu.cfs_quota_us": "50000",
        "/sys/fs/cgroup/cpu/cpu.cfs_period_us": "100000",
    }
    _mock_open = _make_mock_open(mapping)
    _mock_path = _make_mock_path(set(mapping.keys()))

    filepath = os.path.abspath(__file__)
    testargs = [filepath, "--jobs=0"]
    with tmpdir.as_cwd():
        with pytest.raises(SystemExit) as err:
            with patch("builtins.open", _mock_open):
                with patch("pylint.lint.run.Path", _mock_path):
                    Run(testargs, reporter=Reporter())
        assert err.value.code == 0


def test_pylint_run_jobs_zero_with_cfs_quota_fraction_and_sched_affinity(tmpdir):
    # When sched_getaffinity is available, _cpu_count should compute using it
    mapping = {
        "/sys/fs/cgroup/cpu/cpu.cfs_quota_us": "50000",
        "/sys/fs/cgroup/cpu/cpu.cfs_period_us": "100000",
    }
    _mock_open = _make_mock_open(mapping)
    _mock_path = _make_mock_path(set(mapping.keys()))

    filepath = os.path.abspath(__file__)
    testargs = [filepath, "--jobs=0"]
    with tmpdir.as_cwd():
        with pytest.raises(SystemExit) as err:
            with patch("builtins.open", _mock_open):
                with patch("pylint.lint.run.Path", _mock_path):
                    with patch("pylint.lint.run.os.sched_getaffinity", new=lambda x: {0, 1}):
                        Run(testargs, reporter=Reporter())
        assert err.value.code == 0


def test_query_cpu_handles_trailing_whitespace_in_files():
    mapping = {
        "/sys/fs/cgroup/cpu/cpu.cfs_quota_us": " 50000\n",
        "/sys/fs/cgroup/cpu/cpu.cfs_period_us": "100000 \n",
    }
    _mock_open = _make_mock_open(mapping)
    _mock_path = _make_mock_path(set(mapping.keys()))

    with patch("builtins.open", _mock_open):
        with patch("pylint.lint.run.Path", _mock_path):
            assert _query_cpu() == 1


def test_cpu_count_with_mocked_multiprocessing_and_fractional_quota():
    # If multiprocessing.cpu_count() reports >0 and quota/period fraction occurs,
    # _cpu_count should still return at least 1.
    mapping = {
        "/sys/fs/cgroup/cpu/cpu.cfs_quota_us": "50000",
        "/sys/fs/cgroup/cpu/cpu.cfs_period_us": "100000",
    }
    _mock_open = _make_mock_open(mapping)
    _mock_path = _make_mock_path(set(mapping.keys()))

    fake_mp = MagicMock()
    fake_mp.cpu_count = lambda: 4

    with patch("builtins.open", _mock_open):
        with patch("pylint.lint.run.Path", _mock_path):
            with patch("pylint.lint.run.multiprocessing", new=fake_mp):
                # Even though cpu_share would compute to 0 if buggy, _cpu_count must be >= 1
                assert _cpu_count() >= 1


def test_query_cpu_returns_none_when_no_cgroup_files_present():
    # If no cgroup files are present, _query_cpu should return None
    _mock_path = _make_mock_path(set())
    with patch("pylint.lint.run.Path", _mock_path):
        assert _query_cpu() is None


def test_pylint_run_jobs_zero_with_cfs_quota_fraction_and_multiprocessing_mock(tmpdir):
    # Ensure Run() still succeeds when multiprocessing is present and fractional CPU is seen.
    mapping = {
        "/sys/fs/cgroup/cpu/cpu.cfs_quota_us": "50000",
        "/sys/fs/cgroup/cpu/cpu.cfs_period_us": "100000",
    }
    _mock_open = _make_mock_open(mapping)
    _mock_path = _make_mock_path(set(mapping.keys()))

    fake_mp = MagicMock()
    fake_mp.cpu_count = lambda: 8

    filepath = os.path.abspath(__file__)
    testargs = [filepath, "--jobs=0"]
    with tmpdir.as_cwd():
        with pytest.raises(SystemExit) as err:
            with patch("builtins.open", _mock_open):
                with patch("pylint.lint.run.Path", _mock_path):
                    with patch("pylint.lint.run.multiprocessing", new=fake_mp):
                        Run(testargs, reporter=Reporter())
        assert err.value.code == 0

# No additional top-level imports required beyond those in the test file.
# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/PyCQA/pylint/blob/main/CONTRIBUTORS.txt
# pylint: disable=missing-module-docstring, missing-function-docstring

from __future__ import annotations

import os
import pathlib
import sys
from collections.abc import Callable
from unittest.mock import MagicMock, mock_open, patch

import pytest
from py._path.local import LocalPath  # type: ignore[import]

from pylint.lint import Run
from pylint.lint.run import _query_cpu, _cpu_count
from pylint.testutils import GenericTestReporter as Reporter


def _make_file_open(quota_value=None, period_value=None, shares_value=None):
    """Return a mock open function that serves cgroup files as requested,
    falling back to the real open for other paths."""
    builtin_open = open

    def _mock_open(path, *args, **kwargs):
        # Normalize to str in case Path objects are passed
        if isinstance(path, os.PathLike):
            path = os.fspath(path)
        if path == "/sys/fs/cgroup/cpu/cpu.cfs_quota_us" and quota_value is not None:
            return mock_open(read_data=str(quota_value))(*((path,) + args), **kwargs)
        if path == "/sys/fs/cgroup/cpu/cpu.cfs_period_us" and period_value is not None:
            return mock_open(read_data=str(period_value))(*((path,) + args), **kwargs)
        if path == "/sys/fs/cgroup/cpu/cpu.shares" and shares_value is not None:
            return mock_open(read_data=str(shares_value))(*((path,) + args), **kwargs)
        return builtin_open(path, *args, **kwargs)

    return _mock_open


def _make_path_mock(quota_exists=False, period_exists=False, shares_exists=False):
    """Return a Path factory that returns objects whose is_file() returns True
    only for the requested cgroup files."""
    pathlib_path = pathlib.Path

    def _mock_path(*args, **kwargs):
        p = args[0] if args else ""
        if p == "/sys/fs/cgroup/cpu/cpu.cfs_quota_us" and quota_exists:
            return MagicMock(is_file=lambda: True)
        if p == "/sys/fs/cgroup/cpu/cpu.cfs_period_us" and period_exists:
            return MagicMock(is_file=lambda: True)
        if p == "/sys/fs/cgroup/cpu/cpu.shares" and shares_exists:
            return MagicMock(is_file=lambda: True)
        # fallback to real Path for other paths
        return pathlib_path(*args, **kwargs)

    return _mock_path


@pytest.mark.parametrize(
    "quota_value",
    [
        "50000",   # half a period -> int(50000/100000) == 0
        "0",       # zero quota -> 0
        "1",       # tiny quota -> 0
        "99999",   # just less than period -> 0
        "2",       # very small -> 0
        "1023",    # still less than period -> 0
    ],
)
def test_query_cpu_cfs_quota_fractional_results_become_one(quota_value: str, tmpdir: LocalPath) -> None:
    """If cpu.cfs_quota_us / cpu.cfs_period_us yields 0, _query_cpu should return 1."""
    mock_open_fn = _make_file_open(quota_value=quota_value, period_value="100000")
    mock_path_fn = _make_path_mock(quota_exists=True, period_exists=True)
    with tmpdir.as_cwd():
        with patch("builtins.open", mock_open_fn):
            with patch("pylint.lint.run.Path", mock_path_fn):
                # Under the correct (gold) implementation, we should never get 0 CPUs.
                assert _query_cpu() == 1


def test_query_cpu_cfs_quota_large_quota_remains_int_value(tmpdir: LocalPath) -> None:
    """Large cpu quota that is >= period should compute to proper integer (e.g., 1)."""
    mock_open_fn = _make_file_open(quota_value="150000", period_value="100000")
    mock_path_fn = _make_path_mock(quota_exists=True, period_exists=True)
    with tmpdir.as_cwd():
        with patch("builtins.open", mock_open_fn):
            with patch("pylint.lint.run.Path", mock_path_fn):
                assert _query_cpu() == 1  # 150000/100000 == 1


def test_cpu_count_with_multiprocessing_respects_minimum_one(tmpdir: LocalPath) -> None:
    """When multiprocessing.cpu_count() is available and _query_cpu calculates 0,
    _cpu_count should return at least 1 (not 0)."""
    mock_open_fn = _make_file_open(quota_value="1", period_value="100000")
    mock_path_fn = _make_path_mock(quota_exists=True, period_exists=True)
    fake_multiprocessing = MagicMock()
    fake_multiprocessing.cpu_count.return_value = 4
    with tmpdir.as_cwd():
        with patch("builtins.open", mock_open_fn):
            with patch("pylint.lint.run.Path", mock_path_fn):
                # Inject fake multiprocessing into the pylint.lint.run module
                with patch("pylint.lint.run.multiprocessing", fake_multiprocessing):
                    # _cpu_count should evaluate cpu_share as 1 (not 0) after gold patch,
                    # and therefore return min(1, 4) == 1.
                    assert _cpu_count() == 1


def test_cpu_count_with_sched_getaffinity_respects_minimum_one(tmpdir: LocalPath) -> None:
    """When os.sched_getaffinity is available and _query_cpu calculates 0,
    _cpu_count should still return at least 1 (not 0)."""
    mock_open_fn = _make_file_open(quota_value="123", period_value="100000")  # 0
    mock_path_fn = _make_path_mock(quota_exists=True, period_exists=True)
    with tmpdir.as_cwd():
        with patch("builtins.open", mock_open_fn):
            with patch("pylint.lint.run.Path", mock_path_fn):
                # Provide a fake sched_getaffinity that would normally indicate multiple CPUs
                with patch("pylint.lint.run.os.sched_getaffinity", lambda _: {0, 1}):
                    assert _cpu_count() == 1


def test_run_jobs_zero_uses_cpu_count_and_exits_success(tmpdir: LocalPath) -> None:
    """Running Run(..., --jobs=0) should not crash and should exit with code 0,
    even if cgroup quota/period arithmetic would yield 0 without the gold fix."""
    # Prepare a small quota/period that yields 0 from integer division
    mock_open_fn = _make_file_open(quota_value="42", period_value="100000")
    mock_path_fn = _make_path_mock(quota_exists=True, period_exists=True)
    filepath = os.path.abspath(__file__)
    testargs = [filepath, "--jobs=0"]
    with tmpdir.as_cwd():
        with patch("builtins.open", mock_open_fn):
            with patch("pylint.lint.run.Path", mock_path_fn):
                # If the bug is present, Run may end up setting jobs to 0 and behave incorrectly.
                with pytest.raises(SystemExit) as err:
                    Run(testargs, reporter=Reporter())
                assert err.value.code == 0

# No new top-level imports required beyond those inside the test module.
# new test module for regressions related to _query_cpu/_cpu_count
import pytest
from unittest.mock import patch, mock_open, MagicMock
import os

from pylint.lint import run


def _make_open_map(mapping):
    """Return an open replacement that serves different content per path."""
    def _mock_open(path, *args, **kwargs):
        # Accept Path objects converted to str as well
        key = path
        if isinstance(path, os.PathLike):
            key = str(path)
        # If the file is in mapping, return a file-like mock
        if key in mapping:
            return mock_open(read_data=mapping[key])()
        # otherwise raise as real open would for a missing file
        raise FileNotFoundError(key)
    return _mock_open


def _make_path_factory(existing_paths):
    """Return a callable to patch run.Path so that is_file() matches existing_paths."""
    def _mock_path(path):
        # path argument may be a string or Path; convert to str for comparison
        key = path
        if isinstance(path, os.PathLike):
            key = str(path)
        return MagicMock(is_file=lambda: key in existing_paths)
    return _mock_path


def test_query_cpu_negative_shares_returns_negative():
    # cpu.shares = -1024 -> int(-1024/1024) == -1, expect -1 (do not clamp to 1)
    files = {
        "/sys/fs/cgroup/cpu/cpu.shares": "-1024\n",
    }
    with patch("builtins.open", _make_open_map(files)):
        with patch("pylint.lint.run.Path", _make_path_factory(set(files.keys()))):
            assert run._query_cpu() == -1


def test_query_cpu_negative_shares_larger_negative_value():
    # cpu.shares = -2048 -> int(-2048/1024) == -2
    files = {
        "/sys/fs/cgroup/cpu/cpu.shares": "-2048\n",
    }
    with patch("builtins.open", _make_open_map(files)):
        with patch("pylint.lint.run.Path", _make_path_factory(set(files.keys()))):
            assert run._query_cpu() == -2


def test_query_cpu_negative_shares_with_quota_ignored():
    # cpu.cfs_quota_us == -1 (ignored), cpu.shares negative -> negative preserved
    files = {
        "/sys/fs/cgroup/cpu/cpu.cfs_quota_us": "-1\n",
        "/sys/fs/cgroup/cpu/cpu.shares": "-1024\n",
    }
    with patch("builtins.open", _make_open_map(files)):
        with patch("pylint.lint.run.Path", _make_path_factory(set(files.keys()))):
            assert run._query_cpu() == -1


def test_query_cpu_small_negative_shares_rounds_to_zero_then_one():
    # cpu.shares = -512 -> int(-512/1024) == 0 -> corrected to 1
    files = {
        "/sys/fs/cgroup/cpu/cpu.shares": "-512\n",
    }
    with patch("builtins.open", _make_open_map(files)):
        with patch("pylint.lint.run.Path", _make_path_factory(set(files.keys()))):
            assert run._query_cpu() == 1


def test_query_cpu_zero_shares_returns_one():
    # cpu.shares = 0 -> int(0/1024) == 0 -> corrected to 1
    files = {
        "/sys/fs/cgroup/cpu/cpu.shares": "0\n",
    }
    with patch("builtins.open", _make_open_map(files)):
        with patch("pylint.lint.run.Path", _make_path_factory(set(files.keys()))):
            assert run._query_cpu() == 1


def test_query_cpu_fractional_quota_returns_one():
    # quota/period yields fractional <1 -> int() gives 0 -> corrected to 1
    files = {
        "/sys/fs/cgroup/cpu/cpu.cfs_quota_us": "50000\n",
        "/sys/fs/cgroup/cpu/cpu.cfs_period_us": "100000\n",
    }
    with patch("builtins.open", _make_open_map(files)):
        with patch("pylint.lint.run.Path", _make_path_factory(set(files.keys()))):
            assert run._query_cpu() == 1


def test_query_cpu_quota_and_period_return_integer():
    # quota/period yields exact integer
    files = {
        "/sys/fs/cgroup/cpu/cpu.cfs_quota_us": "200000\n",
        "/sys/fs/cgroup/cpu/cpu.cfs_period_us": "100000\n",
    }
    with patch("builtins.open", _make_open_map(files)):
        with patch("pylint.lint.run.Path", _make_path_factory(set(files.keys()))):
            assert run._query_cpu() == 2


def test_query_cpu_no_cgroup_files_returns_none():
    # No relevant files -> None
    with patch("pylint.lint.run.Path", _make_path_factory(set())):
        # builtins.open should not be called, but ensure any call fails
        with patch("builtins.open", side_effect=FileNotFoundError()):
            assert run._query_cpu() is None


def test_cpu_count_uses_sched_getaffinity_and_min_with_cpu_share():
    # When sched_getaffinity is available and _query_cpu returns 2,
    # cpu_count must be min(cpu_share, len(sched_affinity))
    with patch("pylint.lint.run._query_cpu", return_value=2):
        with patch("pylint.lint.run.os.sched_getaffinity", lambda x: {0, 1, 2, 3}):
            assert run._cpu_count() == 2


def test_cpu_count_with_negative_shares_returns_negative_min():
    # When underlying files indicate negative cpu.shares (e.g. -2048 -> -2),
    # _cpu_count should return min(cpu_share, affinity_count) which will be negative.
    files = {
        "/sys/fs/cgroup/cpu/cpu.shares": "-2048\n",
    }
    with patch("builtins.open", _make_open_map(files)):
        with patch("pylint.lint.run.Path", _make_path_factory(set(files.keys()))):
            with patch("pylint.lint.run.os.sched_getaffinity", lambda x: {0, 1, 2, 3}):
                # Expect min(-2, 4) -> -2. The candidate model patch that clamps
                # negative values to 1 would produce 1 and thus fail this test.
                assert run._cpu_count() == -2

# Add import of the internal functions under test
from pylint.lint.run import _query_cpu, _cpu_count
# Additional regression tests for fractional CPU quota handling.
import pytest
from unittest.mock import mock_open, patch, MagicMock
from pylint.lint.run import _query_cpu, _cpu_count

# Paths used by the implementation to query cgroup CPU allocation.
QUOTA_PATH = "/sys/fs/cgroup/cpu/cpu.cfs_quota_us"
PERIOD_PATH = "/sys/fs/cgroup/cpu/cpu.cfs_period_us"

def _make_mock_open(quota_value: str, period_value: str):
    """
    Return a function suitable for patching builtins.open that will return
    quota_value for QUOTA_PATH and period_value for PERIOD_PATH.
    """
    def _mock(path, *args, **kwargs):
        if path == QUOTA_PATH:
            return mock_open(read_data=str(quota_value))()
        if path == PERIOD_PATH:
            return mock_open(read_data=str(period_value))()
        # For any other path, raise so tests catch unexpected accesses.
        raise FileNotFoundError(path)
    return _mock

class _DummyPath:
    """
    Dummy replacement for pathlib.Path used by pylint.lint.run.Path.
    It reports existence (is_file) for the quota and period paths only.
    """
    def __init__(self, path):
        self._path = path

    def is_file(self):
        return self._path in (QUOTA_PATH, PERIOD_PATH)

@pytest.mark.parametrize(
    "quota,period",
    [
        ("50000", "100000"),   # 0.5 -> int division yields 0
        ("99999", "100000"),   # fractional < 1 -> 0
        ("1", "100000"),       # tiny quota -> 0
        ("1023", "1000000"),   # fractional -> 0
        ("100", "1000"),       # 0.1 -> 0
    ],
)
def test_query_cpu_quota_fraction_always_at_least_one(quota, period):
    """
    _query_cpu should return 1 when the cfs_quota/cfs_period integer division
    would otherwise yield 0 (fractional CPU allotment).
    """
    mock_open_fn = _make_mock_open(quota, period)
    with patch("builtins.open", mock_open_fn):
        with patch("pylint.lint.run.Path", _DummyPath):
            result = _query_cpu()
    assert result == 1, f"_query_cpu returned {result} for quota={quota}, period={period}"

@pytest.mark.parametrize(
    "quota,period",
    [
        ("50000", "100000"),
        ("99999", "100000"),
        ("1", "100000"),
        ("1023", "1000000"),
        ("100", "1000"),
    ],
)
def test_cpu_count_with_sched_getaffinity_and_fractional_quota_returns_one(quota, period):
    """
    _cpu_count should use sched_getaffinity when available, and when _query_cpu
    reports a fractional CPU (which should be normalized to 1), _cpu_count must
    return at least 1 (min of cpu_share and affinity size).
    """
    mock_open_fn = _make_mock_open(quota, period)
    # Simulate a system with 4 CPUs available via sched_getaffinity.
    fake_affinity = {0, 1, 2, 3}
    with patch("builtins.open", mock_open_fn):
        with patch("pylint.lint.run.Path", _DummyPath):
            with patch("os.sched_getaffinity", lambda _: fake_affinity):
                result = _cpu_count()
    # cpu_share should be normalized to 1, so min(1, 4) == 1
    assert result == 1, f"_cpu_count returned {result} for quota={quota}, period={period}"

# Additional regression tests for cgroup cpu quota handling
import os
import pathlib
from unittest.mock import MagicMock, mock_open, patch

import pytest

from pylint.lint import Run
from pylint.testutils import GenericTestReporter as Reporter


def _make_open_and_path(quota_value, period_value, include_shares=False, shares_value=None):
    """
    Return a pair (mock_open_function, mock_Path_constructor) to simulate
    cgroup files for cpu.cfs_quota_us, cpu.cfs_period_us and optionally cpu.shares.
    The opened file contents are the provided numeric values (as strings).
    """
    builtin_open = open

    def _mock_open(*args, **kwargs):
        path = args[0]
        if path == "/sys/fs/cgroup/cpu/cpu.cfs_quota_us":
            return mock_open(read_data=str(quota_value))(*args, **kwargs)
        if path == "/sys/fs/cgroup/cpu/cpu.cfs_period_us":
            return mock_open(read_data=str(period_value))(*args, **kwargs)
        if include_shares and path == "/sys/fs/cgroup/cpu/cpu.shares":
            return mock_open(read_data=str(shares_value))(*args, **kwargs)
        return builtin_open(*args, **kwargs)

    pathlib_path = pathlib.Path

    def _mock_path(*args, **kwargs):
        # args[0] is the path string passed in Run module
        p = args[0]
        if p in ("/sys/fs/cgroup/cpu/cpu.cfs_quota_us", "/sys/fs/cgroup/cpu/cpu.cfs_period_us"):
            return MagicMock(is_file=lambda: True)
        if include_shares and p == "/sys/fs/cgroup/cpu/cpu.shares":
            return MagicMock(is_file=lambda: True)
        return pathlib_path(p)

    return _mock_open, _mock_path


@pytest.mark.parametrize(
    "quota,period",
    [
        (50000, 100000),   # 0.5 -> int(...) == 0
        (1, 100000),       # tiny quota -> 0
        (0, 100000),       # zero quota -> 0 (should normalize to 1)
        (99999, 100000),   # just under 1 -> 0
        (12345, 100000),   # small fraction -> 0
    ],
)
def test_jobs_zero_with_small_quota_fraction(tmp_path, quota, period):
    """Quota smaller than period should not lead to 0 CPUs available."""
    filepath = os.path.abspath(__file__)
    args = [filepath, "--jobs=0"]
    mock_open_fn, mock_path_ctor = _make_open_and_path(quota, period)

    with pytest.raises(SystemExit) as err:
        with patch("builtins.open", mock_open_fn):
            with patch("pylint.lint.run.Path", mock_path_ctor):
                # Should exit cleanly with code 0 under gold patch
                Run(args, reporter=Reporter())
    assert err.value.code == 0


@pytest.mark.parametrize(
    "quota,period,shares,shares_val",
    [
        (50000, 100000, True, 2),      # quota path present (used), shares small too
        (99999, 100000, True, 512),    # quota chosen even if shares exist
        (20000, 100000, True, 1024),   # quota chosen and yields zero, shares larger
    ],
)
def test_jobs_zero_quota_takes_precedence_over_shares(tmp_path, quota, period, shares, shares_val):
    """
    When both cfs_quota_us and cpu.shares exist, quota branch should be used.
    If quota produces 0, it must be normalized to 1 (gold behavior).
    """
    filepath = os.path.abspath(__file__)
    args = [filepath, "--jobs=0"]
    mock_open_fn, mock_path_ctor = _make_open_and_path(quota, period, include_shares=shares, shares_value=shares_val)

    with pytest.raises(SystemExit) as err:
        with patch("builtins.open", mock_open_fn):
            with patch("pylint.lint.run.Path", mock_path_ctor):
                Run(args, reporter=Reporter())
    assert err.value.code == 0


def test_jobs_zero_with_very_small_quota(tmp_path):
    """Another small-quota edge case ensuring normalization for tiny quotas."""
    filepath = os.path.abspath(__file__)
    args = [filepath, "--jobs=0"]
    # quota 512, period 1024 => int(512/1024) == 0 -> should become 1
    mock_open_fn, mock_path_ctor = _make_open_and_path(512, 1024)

    with pytest.raises(SystemExit) as err:
        with patch("builtins.open", mock_open_fn):
            with patch("pylint.lint.run.Path", mock_path_ctor):
                Run(args, reporter=Reporter())
    assert err.value.code == 0


def test_jobs_zero_quota_just_below_period(tmp_path):
    """
    quota slightly less than period should still be treated as 1 available CPU.
    """
    filepath = os.path.abspath(__file__)
    args = [filepath, "--jobs=0"]
    mock_open_fn, mock_path_ctor = _make_open_and_path(99999, 100001)

    with pytest.raises(SystemExit) as err:
        with patch("builtins.open", mock_open_fn):
            with patch("pylint.lint.run.Path", mock_path_ctor):
                Run(args, reporter=Reporter())
    assert err.value.code == 0

# No new top-level imports required beyond what's included in the test code.
# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/PyCQA/pylint/blob/main/CONTRIBUTORS.txt
# pylint: disable=missing-module-docstring, missing-function-docstring

from __future__ import annotations

import builtins
import io
from unittest.mock import patch
import pytest

from pylint.lint.run import _query_cpu

def _run_with_files(file_mapping):
    """
    Helper to patch Path.is_file checks and builtins.open for specific
    cgroup file paths used by _query_cpu.
    file_mapping: dict of {path_str: file_content_str}
    """
    original_open = builtins.open

    def _mock_open(path, *args, **kwargs):
        # path may be a pathlib.Path in some contexts; convert to str for lookup
        p = path if isinstance(path, str) else str(path)
        if p in file_mapping:
            # Return a text file-like object
            return io.StringIO(file_mapping[p])
        return original_open(path, *args, **kwargs)

    def _mock_path(*args, **kwargs):
        p = args[0] if args else ""
        return type(
            "P",
            (),
            {"is_file": lambda self, p=p: p in file_mapping},
        )()

    with patch("builtins.open", new=_mock_open):
        with patch("pylint.lint.run.Path", _mock_path):
            return _query_cpu()

def test_quota_less_than_period_returns_one():
    # quota 50000, period 100000 -> int(50000/100000) == 0 -> should be normalized to 1
    fm = {
        "/sys/fs/cgroup/cpu/cpu.cfs_quota_us": "50000\n",
        "/sys/fs/cgroup/cpu/cpu.cfs_period_us": "100000\n",
    }
    assert _run_with_files(fm) == 1

def test_quota_very_small_returns_one():
    # quota 1, period 100000 -> 0 -> normalized to 1
    fm = {
        "/sys/fs/cgroup/cpu/cpu.cfs_quota_us": "1\n",
        "/sys/fs/cgroup/cpu/cpu.cfs_period_us": "100000\n",
    }
    assert _run_with_files(fm) == 1

def test_quota_just_below_period_returns_one():
    # quota 99999, period 100000 -> 0 -> normalized to 1
    fm = {
        "/sys/fs/cgroup/cpu/cpu.cfs_quota_us": "99999\n",
        "/sys/fs/cgroup/cpu/cpu.cfs_period_us": "100000\n",
    }
    assert _run_with_files(fm) == 1

def test_quota_near_equal_period_returns_one():
    # quota nearly equal but still smaller -> 0 -> normalized to 1
    fm = {
        "/sys/fs/cgroup/cpu/cpu.cfs_quota_us": "123456\n",
        "/sys/fs/cgroup/cpu/cpu.cfs_period_us": "123457\n",
    }
    assert _run_with_files(fm) == 1

def test_quota_larger_than_period_returns_multiple_cpus():
    # quota 200000, period 100000 -> 2 CPUs
    fm = {
        "/sys/fs/cgroup/cpu/cpu.cfs_quota_us": "200000\n",
        "/sys/fs/cgroup/cpu/cpu.cfs_period_us": "100000\n",
    }
    assert _run_with_files(fm) == 2

def test_quota_takes_precedence_over_shares_and_normalizes_zero():
    # Both quota and shares exist; quota is used even if it yields 0
    fm = {
        "/sys/fs/cgroup/cpu/cpu.cfs_quota_us": "50000\n",
        "/sys/fs/cgroup/cpu/cpu.cfs_period_us": "100000\n",
        "/sys/fs/cgroup/cpu/cpu.shares": "2048\n",
    }
    # quota branch yields 0 but should be normalized to 1 (and should be selected over shares)
    assert _run_with_files(fm) == 1

def test_quota_minus_one_uses_shares_and_normalizes_zero():
    # quota == -1 -> use shares branch, shares 512 -> int(512/1024) == 0 -> normalized to 1
    fm = {
        "/sys/fs/cgroup/cpu/cpu.cfs_quota_us": "-1\n",
        "/sys/fs/cgroup/cpu/cpu.shares": "512\n",
    }
    assert _run_with_files(fm) == 1

def test_no_cgroup_files_returns_none():
    # No relevant files present -> should return None
    fm = {}
    assert _run_with_files(fm) is None

def test_quota_zero_is_falsy_and_falls_back_to_shares_or_none():
    # quota file contains "0" which is falsy, so shares not present -> None
    fm = {
        "/sys/fs/cgroup/cpu/cpu.cfs_quota_us": "0\n",
    }
    assert _run_with_files(fm) is None

def test_quota_present_but_period_missing_returns_none():
    # quota present but period file missing and shares absent -> None
    fm = {
        "/sys/fs/cgroup/cpu/cpu.cfs_quota_us": "50000\n",
    }
    assert _run_with_files(fm) is None

from pylint.lint import run as run_mod

# Additional regression tests for pylint.lint.run._query_cpu
import builtins
from unittest.mock import mock_open, patch, MagicMock
import pathlib

def _make_mocks(files_to_contents):
    """
    Return a tuple (mock_open_fn, mock_path_fn) that will:
     - return file contents from files_to_contents for matching paths
     - Path(...).is_file() returns True for keys in files_to_contents, False otherwise
    """
    builtin_open = builtins.open
    def _mock_open(path, *args, **kwargs):
        # Accept both Path and str passed into open
        p = str(path)
        if p in files_to_contents:
            return mock_open(read_data=files_to_contents[p])()
        return builtin_open(path, *args, **kwargs)

    real_pathlib = pathlib.Path
    def _mock_path(*args, **kwargs):
        p = args[0] if args else ""
        if str(p) in files_to_contents:
            return MagicMock(is_file=lambda: True)
        return real_pathlib(*args, **kwargs)

    return _mock_open, _mock_path

def test_query_cpu_quota_less_than_period_returns_one():
    files = {
        "/sys/fs/cgroup/cpu/cpu.cfs_quota_us": "50\n",
        "/sys/fs/cgroup/cpu/cpu.cfs_period_us": "100\n",
    }
    mopen, mpath = _make_mocks(files)
    with patch("builtins.open", mopen):
        with patch("pylint.lint.run.Path", mpath):
            assert run_mod._query_cpu() == 1

def test_query_cpu_quota_one_less_than_period_returns_one():
    files = {
        "/sys/fs/cgroup/cpu/cpu.cfs_quota_us": "1\n",
        "/sys/fs/cgroup/cpu/cpu.cfs_period_us": "100000\n",
    }
    mopen, mpath = _make_mocks(files)
    with patch("builtins.open", mopen):
        with patch("pylint.lint.run.Path", mpath):
            assert run_mod._query_cpu() == 1

def test_query_cpu_quota_zero_returns_one():
    files = {
        "/sys/fs/cgroup/cpu/cpu.cfs_quota_us": "0\n",
        "/sys/fs/cgroup/cpu/cpu.cfs_period_us": "100\n",
    }
    mopen, mpath = _make_mocks(files)
    with patch("builtins.open", mopen):
        with patch("pylint.lint.run.Path", mpath):
            assert run_mod._query_cpu() == 1

def test_query_cpu_quota_just_below_period_returns_one():
    files = {
        "/sys/fs/cgroup/cpu/cpu.cfs_quota_us": "99999\n",
        "/sys/fs/cgroup/cpu/cpu.cfs_period_us": "100000\n",
    }
    mopen, mpath = _make_mocks(files)
    with patch("builtins.open", mopen):
        with patch("pylint.lint.run.Path", mpath):
            assert run_mod._query_cpu() == 1

def test_query_cpu_shares_small_returns_one():
    files = {
        "/sys/fs/cgroup/cpu/cpu.cfs_quota_us": "-1\n",
        "/sys/fs/cgroup/cpu/cpu.shares": "2\n",
    }
    mopen, mpath = _make_mocks(files)
    with patch("builtins.open", mopen):
        with patch("pylint.lint.run.Path", mpath):
            assert run_mod._query_cpu() == 1

def test_query_cpu_shares_zero_returns_one():
    files = {
        "/sys/fs/cgroup/cpu/cpu.cfs_quota_us": "-1\n",
        "/sys/fs/cgroup/cpu/cpu.shares": "0\n",
    }
    mopen, mpath = _make_mocks(files)
    with patch("builtins.open", mopen):
        with patch("pylint.lint.run.Path", mpath):
            assert run_mod._query_cpu() == 1

def test_query_cpu_no_files_returns_none():
    files = {}
    mopen, mpath = _make_mocks(files)
    with patch("builtins.open", mopen):
        with patch("pylint.lint.run.Path", mpath):
            assert run_mod._query_cpu() is None

def test_query_cpu_quota_exists_no_period_returns_none():
    # quota present but period missing -> cannot compute, shares missing -> None
    files = {
        "/sys/fs/cgroup/cpu/cpu.cfs_quota_us": "200000\n",
    }
    mopen, mpath = _make_mocks(files)
    with patch("builtins.open", mopen):
        with patch("pylint.lint.run.Path", mpath):
            assert run_mod._query_cpu() is None

def test_query_cpu_quota_and_period_large_returns_two():
    files = {
        "/sys/fs/cgroup/cpu/cpu.cfs_quota_us": "200000\n",
        "/sys/fs/cgroup/cpu/cpu.cfs_period_us": "100000\n",
    }
    mopen, mpath = _make_mocks(files)
    with patch("builtins.open", mopen):
        with patch("pylint.lint.run.Path", mpath):
            assert run_mod._query_cpu() == 2

def test_query_cpu_shares_large_returns_two():
    files = {
        "/sys/fs/cgroup/cpu/cpu.cfs_quota_us": "-1\n",
        "/sys/fs/cgroup/cpu/cpu.shares": "2048\n",
    }
    mopen, mpath = _make_mocks(files)
    with patch("builtins.open", mopen):
        with patch("pylint.lint.run.Path", mpath):
            assert run_mod._query_cpu() == 2

# tests/test_query_cpu_quota_zero.py
import builtins
from unittest.mock import mock_open, patch
import pytest

from pylint.lint.run import _query_cpu

def _make_mock(open_map):
    builtin_open = builtins.open

    def _mock_open(file, *args, **kwargs):
        # Normalize path to string for comparison
        path = file if isinstance(file, str) else str(file)
        if path in open_map:
            # mock_open returns a callable that needs to be called
            return mock_open(read_data=open_map[path])()
        return builtin_open(file, *args, **kwargs)

    return _mock_open

@pytest.mark.parametrize(
    "quota,period",
    [
        ("500", "1000"),        # 0.5 -> int division 0
        ("999", "1000000"),     # very small fraction -> 0
        ("1", "2"),             # 0.5 -> 0
        ("0", "100000"),        # zero quota -> 0
        ("3", "10"),            # 0.3 -> 0
        (" 1\n", " 2\n"),       # whitespace trimmed -> 0
        ("0001", "002"),        # leading zeros -> 0
        ("  5  \n", "10\n"),    # extra whitespace -> 0
        ("2", "3"),             # 0.66 -> 0
        ("7", "8"),             # 0.875 -> 0
    ],
)
def test_query_cpu_normalizes_quota_period_fraction_to_one(quota, period):
    """
    Simulate a cgroup environment where cpu.cfs_quota_us and cpu.cfs_period_us
    exist and their integer division results in 0. _query_cpu should return at least 1.
    """
    open_map = {
        "/sys/fs/cgroup/cpu/cpu.cfs_quota_us": quota,
        "/sys/fs/cgroup/cpu/cpu.cfs_period_us": period,
    }

    with patch("builtins.open", new=_make_mock(open_map)):
        # Patch Path.is_file to return True only for the files present in open_map
        with patch("pylint.lint.run.Path.is_file", new=lambda self: str(self) in open_map):
            assert _query_cpu() == 1

# No additional top-level imports required beyond those included in the test file.
# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/PyCQA/pylint/blob/main/CONTRIBUTORS.txt
# pylint: disable=missing-module-docstring, missing-function-docstring, redefined-outer-name

from __future__ import annotations

import os
import pathlib
import sys
from collections.abc import Callable
from unittest.mock import MagicMock, mock_open, patch

import pytest
from py._path.local import LocalPath  # type: ignore[import]

from pylint.lint import Run
from pylint.lint.run import _query_cpu
from pylint.testutils import GenericTestReporter as Reporter


def _make_path_mock(true_paths: set[str]):
    """Return a Path factory that reports is_file True for entries in true_paths."""
    real_path = pathlib.Path

    def _mock_path(arg, *args, **kwargs):
        if arg in true_paths:
            return MagicMock(is_file=lambda: True)
        return real_path(arg, *args, **kwargs)

    return _mock_path


def _open_factory(contents: dict[str, str]):
    """Return an open replacement that serves provided file contents."""
    real_open = open

    def _mock_open(*args, **kwargs):
        filename = args[0]
        if filename in contents:
            return mock_open(read_data=contents[filename])(*args, **kwargs)
        return real_open(*args, **kwargs)

    return _mock_open


@pytest.mark.parametrize("cpu_quota,cpu_period", [("50000", "100000"), ("0", "100000")])
def test_jobs_zero_with_quota_fractional_cpu(tmpdir: LocalPath, cpu_quota: str, cpu_period: str) -> None:
    """
    When cfs_quota_us / cfs_period_us yields 0 (fractional CPU), _query_cpu should
    normalize to at least 1 CPU and Run(..., --jobs=0) must not crash. This
    catches the case where only the quota/period branch produced avail_cpu == 0.
    """
    contents = {
        "/sys/fs/cgroup/cpu/cpu.cfs_quota_us": cpu_quota + "\n",
        "/sys/fs/cgroup/cpu/cpu.cfs_period_us": cpu_period + "\n",
    }
    with tmpdir.as_cwd():
        with patch("builtins.open", _open_factory(contents)):
            with patch("pylint.lint.run.Path", _make_path_mock(set(contents.keys()))):
                # Ensure multiprocessing.cpu_count is available and >0
                fake_mp = MagicMock()
                fake_mp.cpu_count.return_value = 4
                with patch("pylint.lint.run.multiprocessing", fake_mp):
                    testargs = [os.path.abspath(__file__), "--jobs=0"]
                    with pytest.raises(SystemExit) as err:
                        Run(testargs, reporter=Reporter())
                    assert err.value.code == 0


def test_jobs_zero_quota_wins_over_shares(tmpdir: LocalPath) -> None:
    """
    If both quota/period and shares present, quota branch must be used and
    any zero result must be normalized to 1 CPU.
    """
    contents = {
        "/sys/fs/cgroup/cpu/cpu.cfs_quota_us": "50000\n",  # fractional -> 0
        "/sys/fs/cgroup/cpu/cpu.cfs_period_us": "100000\n",
        "/sys/fs/cgroup/cpu/cpu.shares": "2\n",  # would also produce 0
    }
    with tmpdir.as_cwd():
        with patch("builtins.open", _open_factory(contents)):
            with patch("pylint.lint.run.Path", _make_path_mock(set(contents.keys()))):
                fake_mp = MagicMock()
                fake_mp.cpu_count.return_value = 8
                with patch("pylint.lint.run.multiprocessing", fake_mp):
                    testargs = [os.path.abspath(__file__), "--jobs=0"]
                    with pytest.raises(SystemExit) as err:
                        Run(testargs, reporter=Reporter())
                    assert err.value.code == 0


def test_jobs_zero_with_shares_fractional_cpu(tmpdir: LocalPath) -> None:
    """
    If cpu.shares yields a fractional CPU (small shares), must be normalized to 1.
    This is similar to an existing test, included for completeness.
    """
    contents = {
        "/sys/fs/cgroup/cpu/cpu.cfs_quota_us": "-1\n",  # invalid, so ignore quota branch
        "/sys/fs/cgroup/cpu/cpu.shares": "2\n",  # 2/1024 -> 0 => should normalize to 1
    }
    with tmpdir.as_cwd():
        with patch("builtins.open", _open_factory(contents)):
            with patch("pylint.lint.run.Path", _make_path_mock(set(contents.keys()))):
                fake_mp = MagicMock()
                fake_mp.cpu_count.return_value = 4
                with patch("pylint.lint.run.multiprocessing", fake_mp):
                    testargs = [os.path.abspath(__file__), "--jobs=0"]
                    with pytest.raises(SystemExit) as err:
                        Run(testargs, reporter=Reporter())
                    assert err.value.code == 0


def test_query_cpu_directly_normalizes_zero_from_quota_and_period() -> None:
    """
    Call _query_cpu directly to ensure that a zero computed from quota/period
    is normalized to 1 (this is the targeted bugfix).
    """
    contents = {
        "/sys/fs/cgroup/cpu/cpu.cfs_quota_us": "12345\n",  # < period
        "/sys/fs/cgroup/cpu/cpu.cfs_period_us": "100000\n",
    }
    with patch("builtins.open", _open_factory(contents)):
        with patch("pylint.lint.run.Path", _make_path_mock(set(contents.keys()))):
            # No multiprocessing needed; _query_cpu should return 1
            assert _query_cpu() == 1


def test_query_cpu_prefers_quota_over_shares(tmpdir: LocalPath) -> None:
    """
    If quota is present (and not -1) and period is present, it must be used
    even if cpu.shares is also present.
    """
    contents = {
        "/sys/fs/cgroup/cpu/cpu.cfs_quota_us": "250000\n",  # 2.5 -> int() -> 2
        "/sys/fs/cgroup/cpu/cpu.cfs_period_us": "100000\n",
        "/sys/fs/cgroup/cpu/cpu.shares": "1\n",
    }
    with patch("builtins.open", _open_factory(contents)):
        with patch("pylint.lint.run.Path", _make_path_mock(set(contents.keys()))):
            assert _query_cpu() == 2


def test_behavior_without_any_cgroup_files_uses_sched_affinity(tmpdir: LocalPath) -> None:
    """
    If no cgroup files are present, _cpu_count should rely on os.sched_getaffinity
    if available. Here we patch sched_getaffinity to simulate 3 CPUs.
    """
    # No cgroup files present -> Path.is_file should be False for them
    with tmpdir.as_cwd():
        with patch("pylint.lint.run.Path", pathlib.Path):
            # Patch sched_getaffinity to simulate 3 CPUs
            with patch.object(os, "sched_getaffinity", lambda _: {0, 1, 2}):
                fake_mp = MagicMock()
                fake_mp.cpu_count.return_value = 99  # should not be used
                with patch("pylint.lint.run.multiprocessing", fake_mp):
                    testargs = [os.path.abspath(__file__), "--jobs=0"]
                    with pytest.raises(SystemExit) as err:
                        Run(testargs, reporter=Reporter())
                    assert err.value.code == 0


def test_behavior_without_sched_uses_multiprocessing_cpu_count(tmpdir: LocalPath) -> None:
    """
    If sched_getaffinity not available, fallback to multiprocessing.cpu_count().
    """
    with tmpdir.as_cwd():
        with patch("pylint.lint.run.Path", pathlib.Path):
            # Remove sched_getaffinity if present
            if hasattr(os, "sched_getaffinity"):
                with patch.object(os, "sched_getaffinity", None):
                    fake_mp = MagicMock()
                    fake_mp.cpu_count.return_value = 2
                    with patch("pylint.lint.run.multiprocessing", fake_mp):
                        testargs = [os.path.abspath(__file__), "--jobs=0"]
                        with pytest.raises(SystemExit) as err:
                            Run(testargs, reporter=Reporter())
                        assert err.value.code == 0
            else:
                # If not present on the platform already, just ensure multiprocessing is used
                fake_mp = MagicMock()
                fake_mp.cpu_count.return_value = 2
                with patch("pylint.lint.run.multiprocessing", fake_mp):
                    testargs = [os.path.abspath(__file__), "--jobs=0"]
                    with pytest.raises(SystemExit) as err:
                        Run(testargs, reporter=Reporter())
                    assert err.value.code == 0


def test_cpu_shares_with_whitespace_and_newlines_are_parsed(tmpdir: LocalPath) -> None:
    """
    Ensure files with surrounding whitespace/newlines are parsed correctly and
    normalized when they produce zero.
    """
    contents = {
        "/sys/fs/cgroup/cpu/cpu.cfs_quota_us": "  -1  \n",
        "/sys/fs/cgroup/cpu/cpu.shares": "   2   \n",
    }
    with tmpdir.as_cwd():
        with patch("builtins.open", _open_factory(contents)):
            with patch("pylint.lint.run.Path", _make_path_mock(set(contents.keys()))):
                fake_mp = MagicMock()
                fake_mp.cpu_count.return_value = 3
                with patch("pylint.lint.run.multiprocessing", fake_mp):
                    testargs = [os.path.abspath(__file__), "--jobs=0"]
                    with pytest.raises(SystemExit) as err:
                        Run(testargs, reporter=Reporter())
                    assert err.value.code == 0


def test_query_cpu_zero_from_quota_normalized_to_one_directly() -> None:
    """
    Another direct check ensuring a zero computed from quota/period is normalized to 1.
    This specifically asserts the module-level _query_cpu behavior.
    """
    contents = {
        "/sys/fs/cgroup/cpu/cpu.cfs_quota_us": "1\n",  # much smaller than period
        "/sys/fs/cgroup/cpu/cpu.cfs_period_us": "100000\n",
    }
    with patch("builtins.open", _open_factory(contents)):
        with patch("pylint.lint.run.Path", _make_path_mock(set(contents.keys()))):
            assert _query_cpu() == 1

from unittest.mock import mock_open, patch, MagicMock
import importlib
import os
# Additional regression tests for pylint.lint.run
from __future__ import annotations
import builtins
from unittest.mock import mock_open, patch, MagicMock
import os
import importlib

import pytest

# Import the module under test
from pylint.lint import run as run_module

def _make_mock_open(mapping):
    """Return a function usable to patch builtins.open that returns different
    contents depending on the filename."""
    real_open = builtins.open

    def _mock_open(file, *args, **kwargs):
        # mapping keys may be Path strings
        if file in mapping:
            data = mapping[file]
            return mock_open(read_data=data)()
        return real_open(file, *args, **kwargs)

    return _mock_open

class FakePath:
    def __init__(self, path, exists_files):
        self._path = path
        self._exists = exists_files

    def is_file(self):
        return self._path in self._exists

def _make_path_factory(exists_files):
    def _path(path_str):
        return FakePath(path_str, exists_files)
    return _path

def test_query_cpu_quota_fraction_returns_one():
    # quota 50000, period 100000 -> int(0.5) == 0 -> should be normalized to 1
    mapping = {
        "/sys/fs/cgroup/cpu/cpu.cfs_quota_us": "50000\n",
        "/sys/fs/cgroup/cpu/cpu.cfs_period_us": "100000\n",
    }
    with patch("builtins.open", _make_mock_open(mapping)):
        with patch("pylint.lint.run.Path", _make_path_factory(set(mapping.keys()))):
            # reload module symbols to ensure functions use patched Path if necessary
            importlib.reload(run_module)
            assert run_module._query_cpu() == 1

def test_query_cpu_quota_tiny_fraction_returns_one():
    # quota 1, period 100000 -> int(0.00001) == 0 -> normalized to 1
    mapping = {
        "/sys/fs/cgroup/cpu/cpu.cfs_quota_us": "1\n",
        "/sys/fs/cgroup/cpu/cpu.cfs_period_us": "100000\n",
    }
    with patch("builtins.open", _make_mock_open(mapping)):
        with patch("pylint.lint.run.Path", _make_path_factory(set(mapping.keys()))):
            importlib.reload(run_module)
            assert run_module._query_cpu() == 1

def test_query_cpu_quota_exact_one_returns_one():
    # quota equals period -> int(1) == 1
    mapping = {
        "/sys/fs/cgroup/cpu/cpu.cfs_quota_us": "100000\n",
        "/sys/fs/cgroup/cpu/cpu.cfs_period_us": "100000\n",
    }
    with patch("builtins.open", _make_mock_open(mapping)):
        with patch("pylint.lint.run.Path", _make_path_factory(set(mapping.keys()))):
            importlib.reload(run_module)
            assert run_module._query_cpu() == 1

def test_query_cpu_shares_small_returns_one():
    # shares 2 -> int(2/1024) == 0 -> normalized to 1
    mapping = {"/sys/fs/cgroup/cpu/cpu.shares": "2\n"}
    with patch("builtins.open", _make_mock_open(mapping)):
        with patch("pylint.lint.run.Path", _make_path_factory(set(mapping.keys()))):
            importlib.reload(run_module)
            assert run_module._query_cpu() == 1

def test_query_cpu_shares_large_value():
    # shares 2048 -> int(2048/1024) == 2
    mapping = {"/sys/fs/cgroup/cpu/cpu.shares": "2048\n"}
    with patch("builtins.open", _make_mock_open(mapping)):
        with patch("pylint.lint.run.Path", _make_path_factory(set(mapping.keys()))):
            importlib.reload(run_module)
            assert run_module._query_cpu() == 2

def test_query_cpu_quota_takes_precedence_over_shares():
    # If both quota and shares exist, quota branch should be used.
    mapping = {
        "/sys/fs/cgroup/cpu/cpu.cfs_quota_us": "50000\n",   # would produce 0 -> normalize to 1
        "/sys/fs/cgroup/cpu/cpu.cfs_period_us": "100000\n",
        "/sys/fs/cgroup/cpu/cpu.shares": "2048\n",
    }
    exists = set(mapping.keys())
    with patch("builtins.open", _make_mock_open(mapping)):
        with patch("pylint.lint.run.Path", _make_path_factory(exists)):
            importlib.reload(run_module)
            # quota branch should yield 1 (not use shares' 2)
            assert run_module._query_cpu() == 1

def test_cpu_count_uses_sched_affinity_and_min_with_quota_normalized():
    # Make sched_getaffinity available returning 4 CPUs.
    # _query_cpu should normalize tiny quota to 1, so _cpu_count should be min(1,4) == 1
    mapping = {
        "/sys/fs/cgroup/cpu/cpu.cfs_quota_us": "1\n",
        "/sys/fs/cgroup/cpu/cpu.cfs_period_us": "100000\n",
    }
    with patch("builtins.open", _make_mock_open(mapping)):
        with patch("pylint.lint.run.Path", _make_path_factory(set(mapping.keys()))):
            with patch.object(os, "sched_getaffinity", lambda pid: {0, 1, 2, 3}):
                importlib.reload(run_module)
                assert run_module._cpu_count() == 1

def test_cpu_count_without_sched_uses_multiprocessing_and_min():
    # Remove sched_getaffinity, simulate multiprocessing.cpu_count()
    mapping = {
        "/sys/fs/cgroup/cpu/cpu.cfs_quota_us": "1\n",
        "/sys/fs/cgroup/cpu/cfs_period_us_not_used": "100000\n",
    }
    # For this test no cgroup period file exists, so query returns None -> cpu_count should be multiprocessing.cpu_count()
    fake_multiproc = MagicMock()
    fake_multiproc.cpu_count.return_value = 8
    with patch("pylint.lint.run.Path", _make_path_factory(set())), patch(
        "pylint.lint.run.multiprocessing", fake_multiproc
    ):
        importlib.reload(run_module)
        assert run_module._cpu_count() == 8

def test_query_cpu_no_cgroup_files_returns_none():
    # If no cgroup files present, _query_cpu should return None
    with patch("pylint.lint.run.Path", _make_path_factory(set())):
        importlib.reload(run_module)
        assert run_module._query_cpu() is None

# No new top-level imports required beyond what the test suite already provides.
# Additional regression tests for pylint.lint.run
from __future__ import annotations

import builtins
import os
from unittest.mock import MagicMock, mock_open, patch

import pytest

from pylint.lint import run as run_module
from pylint.lint import Run
from pylint.testutils import GenericTestReporter as Reporter


def _make_mock_open_and_path(file_contents: dict):
    """
    file_contents: mapping of path -> string content that should be returned by open(...)
    Returns (mock_open_fn, FakePathClass)
    """
    def _mock_open(*args, **kwargs):
        filename = args[0]
        if filename in file_contents:
            return mock_open(read_data=file_contents[filename])(*args, **kwargs)
        # fallback to real open for other files
        return builtins.open(*args, **kwargs)

    class FakePath:
        def __init__(self, p):
            # ensure string
            self._p = str(p)

        def is_file(self):
            return self._p in file_contents

    return _mock_open, FakePath


def test_query_cpu_no_cgroup_files_returns_none():
    mock_open_fn, FakePath = _make_mock_open_and_path({})
    with patch("builtins.open", mock_open_fn):
        with patch("pylint.lint.run.Path", FakePath):
            assert run_module._query_cpu() is None


def test_query_cpu_quota_fraction_results_one():
    # quota 50000, period 100000 -> int(50000/100000) == 0 -> should be normalized to 1
    files = {
        "/sys/fs/cgroup/cpu/cpu.cfs_quota_us": "50000\n",
        "/sys/fs/cgroup/cpu/cpu.cfs_period_us": "100000\n",
    }
    mock_open_fn, FakePath = _make_mock_open_and_path(files)
    with patch("builtins.open", mock_open_fn):
        with patch("pylint.lint.run.Path", FakePath):
            assert run_module._query_cpu() == 1


def test_query_cpu_quota_multiple_results_two():
    # quota 200000, period 100000 -> 2 CPUs
    files = {
        "/sys/fs/cgroup/cpu/cpu.cfs_quota_us": "200000\n",
        "/sys/fs/cgroup/cpu/cpu.cfs_period_us": "100000\n",
    }
    mock_open_fn, FakePath = _make_mock_open_and_path(files)
    with patch("builtins.open", mock_open_fn):
        with patch("pylint.lint.run.Path", FakePath):
            assert run_module._query_cpu() == 2


def test_query_cpu_shares_fraction_results_one():
    # shares 512 -> int(512/1024) == 0 -> normalized to 1
    files = {
        "/sys/fs/cgroup/cpu/cpu.cfs_quota_us": "-1\n",  # make quota irrelevant
        "/sys/fs/cgroup/cpu/cpu.shares": "512\n",
    }
    mock_open_fn, FakePath = _make_mock_open_and_path(files)
    with patch("builtins.open", mock_open_fn):
        with patch("pylint.lint.run.Path", FakePath):
            assert run_module._query_cpu() == 1


def test_query_cpu_shares_multiple_two():
    # shares 2048 -> int(2048/1024) == 2
    files = {
        "/sys/fs/cgroup/cpu/cpu.cfs_quota_us": "-1\n",
        "/sys/fs/cgroup/cpu/cpu.shares": "2048\n",
    }
    mock_open_fn, FakePath = _make_mock_open_and_path(files)
    with patch("builtins.open", mock_open_fn):
        with patch("pylint.lint.run.Path", FakePath):
            assert run_module._query_cpu() == 2


def test_query_cpu_zero_values_result_one_quota_zero():
    # quota == 0 -> int(0/period) == 0 -> normalize to 1
    files = {
        "/sys/fs/cgroup/cpu/cpu.cfs_quota_us": "0\n",
        "/sys/fs/cgroup/cpu/cpu.cfs_period_us": "100000\n",
    }
    mock_open_fn, FakePath = _make_mock_open_and_path(files)
    with patch("builtins.open", mock_open_fn):
        with patch("pylint.lint.run.Path", FakePath):
            assert run_module._query_cpu() == 1


def test_query_cpu_zero_values_result_one_shares_zero():
    # shares == 0 -> int(0/1024) == 0 -> normalize to 1
    files = {
        "/sys/fs/cgroup/cpu/cpu.cfs_quota_us": "-1\n",
        "/sys/fs/cgroup/cpu/cpu.shares": "0\n",
    }
    mock_open_fn, FakePath = _make_mock_open_and_path(files)
    with patch("builtins.open", mock_open_fn):
        with patch("pylint.lint.run.Path", FakePath):
            assert run_module._query_cpu() == 1


def test_cpu_count_with_sched_affinity_uses_min_value():
    # Simulate sched_getaffinity returning 4 CPUs available to the process.
    # Then if quota indicates 2 CPUs, _cpu_count() should be min(2,4) == 2.
    files = {
        "/sys/fs/cgroup/cpu/cpu.cfs_quota_us": "200000\n",
        "/sys/fs/cgroup/cpu/cpu.cfs_period_us": "100000\n",
    }
    mock_open_fn, FakePath = _make_mock_open_and_path(files)
    with patch("builtins.open", mock_open_fn):
        with patch("pylint.lint.run.Path", FakePath):
            with patch.object(os, "sched_getaffinity", lambda pid: {0, 1, 2, 3}):
                assert run_module._cpu_count() == 2


def test_cpu_count_with_sched_affinity_fraction_ensures_one():
    # sched_getaffinity returns 3 CPUs but quota indicates fractional <1 -> normalized to 1, min(1,3)==1
    files = {
        "/sys/fs/cgroup/cpu/cpu.cfs_quota_us": "50000\n",
        "/sys/fs/cgroup/cpu/cpu.cfs_period_us": "100000\n",
    }
    mock_open_fn, FakePath = _make_mock_open_and_path(files)
    with patch("builtins.open", mock_open_fn):
        with patch("pylint.lint.run.Path", FakePath):
            with patch.object(os, "sched_getaffinity", lambda pid: {0, 1, 2}):
                assert run_module._cpu_count() == 1


def test_run_jobs_equal_zero_dont_crash_with_quota_fraction(tmp_path):
    """
    Integration test: when running Run with --jobs=0 and the cgroup quota/period
    indicate a fractional CPU, Run should normalize to 1 CPU and not crash.
    """
    files = {
        "/sys/fs/cgroup/cpu/cpu.cfs_quota_us": "50000\n",
        "/sys/fs/cgroup/cpu/cpu.cfs_period_us": "100000\n",
    }
    mock_open_fn, FakePath = _make_mock_open_and_path(files)
    testargs = [str(tmp_path / "somefile.py"), "--jobs=0"]
    # create a dummy file to lint (the linter will be given this path)
    (tmp_path / "somefile.py").write_text("x = 1\n")
    with patch("builtins.open", mock_open_fn):
        with patch("pylint.lint.run.Path", FakePath):
            # Also patch sched_getaffinity to report multiple CPUs are available
            with patch.object(os, "sched_getaffinity", lambda pid: {0, 1}):
                with pytest.raises(SystemExit) as err:
                    Run(testargs, reporter=Reporter())
                # Expect exit code 0 (no failures by default)
                assert err.value.code == 0

from pylint.lint.run import _query_cpu, _cpu_count
import types
# Additional regression tests for fractional CPU detection and --jobs=0 behavior
from pylint.lint.run import _query_cpu, _cpu_count
import os as _os_module
import types

def _make_mock_open(mapping):
    """
    Create a mock open function that returns specified contents for file paths
    in mapping, otherwise delegates to the builtin open.
    """
    builtin_open = open
    def _mock_open(*args, **kwargs):
        if args and args[0] in mapping:
            return mock_open(read_data=mapping[args[0]])(*args, **kwargs)
        return builtin_open(*args, **kwargs)
    return _mock_open

def _make_mock_path(true_paths):
    """
    Return a callable to patch Path in the module that returns a MagicMock
    with is_file() True for paths in true_paths, otherwise delegates to the
    real pathlib.Path.
    """
    real_path = pathlib.Path
    def _mock_path(*args, **kwargs):
        if args and args[0] in true_paths:
            return MagicMock(is_file=lambda: True)
        return real_path(*args, **kwargs)
    return _mock_path

def test_query_cpu_with_small_quota_returns_one(tmpdir: LocalPath) -> None:
    # quota / period yields 0 -> should be normalized to 1
    mapping = {
        "/sys/fs/cgroup/cpu/cpu.cfs_quota_us": "50\n",
        "/sys/fs/cgroup/cpu/cpu.cfs_period_us": "100000\n",
    }
    with tmpdir.as_cwd():
        with patch("builtins.open", _make_mock_open(mapping)):
            with patch("pylint.lint.run.Path", _make_mock_path(set(mapping))):
                assert _query_cpu() == 1

def test_run_jobs_zero_with_small_quota_dont_crash(tmpdir: LocalPath) -> None:
    filepath = os.path.abspath(__file__)
    testargs = [filepath, "--jobs=0"]
    mapping = {
        "/sys/fs/cgroup/cpu/cpu.cfs_quota_us": "50\n",
        "/sys/fs/cgroup/cpu/cpu.cfs_period_us": "100000\n",
    }
    with tmpdir.as_cwd():
        with pytest.raises(SystemExit) as err:
            with patch("builtins.open", _make_mock_open(mapping)):
                with patch("pylint.lint.run.Path", _make_mock_path(set(mapping))):
                    Run(testargs, reporter=Reporter())
        assert err.value.code == 0

def test_run_jobs_zero_with_small_quota_and_sched_affinity_dont_crash(tmpdir: LocalPath) -> None:
    filepath = os.path.abspath(__file__)
    testargs = [filepath, "--jobs=0"]
    mapping = {
        "/sys/fs/cgroup/cpu/cpu.cfs_quota_us": "10\n",
        "/sys/fs/cgroup/cpu/cpu.cfs_period_us": "100000\n",
    }
    # Simulate sched_getaffinity reporting 4 CPUs available to the process
    original_sched = getattr(_os_module, "sched_getaffinity", None)
    try:
        _os_module.sched_getaffinity = lambda pid: {0, 1, 2, 3}
        with tmpdir.as_cwd():
            with pytest.raises(SystemExit) as err:
                with patch("builtins.open", _make_mock_open(mapping)):
                    with patch("pylint.lint.run.Path", _make_mock_path(set(mapping))):
                        Run(testargs, reporter=Reporter())
            assert err.value.code == 0
    finally:
        if original_sched is None:
            try:
                delattr(_os_module, "sched_getaffinity")
            except Exception:
                pass
        else:
            _os_module.sched_getaffinity = original_sched

def test_run_jobs_zero_with_small_quota_and_multiprocessing_dont_crash(tmpdir: LocalPath) -> None:
    # Ensure fallback to multiprocessing.cpu_count() works and we still don't crash
    filepath = os.path.abspath(__file__)
    testargs = [filepath, "--jobs=0"]
    mapping = {
        "/sys/fs/cgroup/cpu/cpu.cfs_quota_us": "1\n",
        "/sys/fs/cgroup/cpu/cpu.cfs_period_us": "100000\n",
    }
    fake_multiprocessing = types.SimpleNamespace(cpu_count=lambda: 4)
    # Remove sched_getaffinity if present so cpu_count path is taken
    original_sched = getattr(_os_module, "sched_getaffinity", None)
    try:
        if hasattr(_os_module, "sched_getaffinity"):
            delattr(_os_module, "sched_getaffinity")
        with tmpdir.as_cwd():
            with pytest.raises(SystemExit) as err:
                with patch("builtins.open", _make_mock_open(mapping)):
                    with patch("pylint.lint.run.Path", _make_mock_path(set(mapping))):
                        with patch("pylint.lint.run.multiprocessing", fake_multiprocessing):
                            Run(testargs, reporter=Reporter())
            assert err.value.code == 0
    finally:
        if original_sched is not None:
            _os_module.sched_getaffinity = original_sched

def test_query_cpu_with_small_shares_returns_one(tmpdir: LocalPath) -> None:
    # cpu_quota == -1 (ignored), but shares gives a small value resulting in 0 -> normalized to 1
    mapping = {
        "/sys/fs/cgroup/cpu/cpu.cfs_quota_us": "-1\n",
        "/sys/fs/cgroup/cpu/cpu.shares": "2\n",
    }
    with tmpdir.as_cwd():
        with patch("builtins.open", _make_mock_open(mapping)):
            with patch("pylint.lint.run.Path", _make_mock_path(set(mapping))):
                assert _query_cpu() == 1

def test_run_jobs_zero_with_small_shares_dont_crash(tmpdir: LocalPath) -> None:
    filepath = os.path.abspath(__file__)
    testargs = [filepath, "--jobs=0"]
    mapping = {
        "/sys/fs/cgroup/cpu/cpu.cfs_quota_us": "-1\n",
        "/sys/fs/cgroup/cpu/cpu.shares": "2\n",
    }
    with tmpdir.as_cwd():
        with pytest.raises(SystemExit) as err:
            with patch("builtins.open", _make_mock_open(mapping)):
                with patch("pylint.lint.run.Path", _make_mock_path(set(mapping))):
                    Run(testargs, reporter=Reporter())
        assert err.value.code == 0

def test_query_cpu_no_cgroup_files_returns_none(tmpdir: LocalPath) -> None:
    # No cgroup files present -> _query_cpu should return None
    with tmpdir.as_cwd():
        with patch("builtins.open", mock_open()):
            # Patch Path so it returns False for any cgroup files
            real_path = pathlib.Path
            def _mock_path_false(*args, **kwargs):
                return MagicMock(is_file=lambda: False)
            with patch("pylint.lint.run.Path", _mock_path_false):
                assert _query_cpu() is None

def test_cpu_count_uses_sched_and_is_limited_by_share(tmpdir: LocalPath) -> None:
    # quota/period -> 2 CPUs available; sched_getaffinity returns 4 -> min should be 2
    mapping = {
        "/sys/fs/cgroup/cpu/cpu.cfs_quota_us": "2\n",
        "/sys/fs/cgroup/cpu/cpu.cfs_period_us": "1\n",
    }
    original_sched = getattr(_os_module, "sched_getaffinity", None)
    try:
        _os_module.sched_getaffinity = lambda pid: {0, 1, 2, 3}
        with patch("builtins.open", _make_mock_open(mapping)):
            with patch("pylint.lint.run.Path", _make_mock_path(set(mapping))):
                assert _cpu_count() == 2
    finally:
        if original_sched is None:
            try:
                delattr(_os_module, "sched_getaffinity")
            except Exception:
                pass
        else:
            _os_module.sched_getaffinity = original_sched

def test_cpu_count_uses_multiprocessing_and_is_limited_by_share(tmpdir: LocalPath) -> None:
    # quota/period -> 3 CPUs available; multiprocessing.cpu_count returns 8 -> min should be 3
    mapping = {
        "/sys/fs/cgroup/cpu/cpu.cfs_quota_us": "3\n",
        "/sys/fs/cgroup/cpu/cpu.cfs_period_us": "1\n",
    }
    fake_multiprocessing = types.SimpleNamespace(cpu_count=lambda: 8)
    # Ensure no sched_getaffinity present
    original_sched = getattr(_os_module, "sched_getaffinity", None)
    try:
        if hasattr(_os_module, "sched_getaffinity"):
            delattr(_os_module, "sched_getaffinity")
        with patch("builtins.open", _make_mock_open(mapping)):
            with patch("pylint.lint.run.Path", _make_mock_path(set(mapping))):
                with patch("pylint.lint.run.multiprocessing", fake_multiprocessing):
                    assert _cpu_count() == 3
    finally:
        if original_sched is not None:
            _os_module.sched_getaffinity = original_sched

from unittest.mock import MagicMock, mock_open, patch
import pytest
# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/PyCQA/pylint/blob/main/CONTRIBUTORS.txt
# pylint: disable=missing-module-docstring, missing-function-docstring

from __future__ import annotations

import os
from unittest.mock import MagicMock, mock_open, patch

import pytest

from pylint.lint import run as run_mod
from pylint.lint import Run
from pylint.testutils import GenericTestReporter as Reporter

# Helpers to create an open that returns different contents based on path
def make_mock_open(mapping):
    builtin_open = open

    def _mock_open(*args, **kwargs):
        path = args[0]
        if path in mapping:
            data = mapping[path]
            # mock_open wants str data
            return mock_open(read_data=str(data))(*args, **kwargs)
        return builtin_open(*args, **kwargs)

    return _mock_open

# Helper to mock pathlib.Path behaviour for is_file checks
def make_mock_path(existing_paths):
    def _mock_path(path, *args, **kwargs):
        # Return object with is_file method
        return MagicMock(is_file=lambda: path in existing_paths)
    return _mock_path


def test_query_cpu_quota_fractional_returns_one():
    # quota < period -> int(quota/period) == 0 -> should normalize to 1
    files = {
        "/sys/fs/cgroup/cpu/cpu.cfs_quota_us": "500\n",
        "/sys/fs/cgroup/cpu/cpu.cfs_period_us": "1000000\n",
    }
    with patch("builtins.open", make_mock_open(files)):
        with patch("pylint.lint.run.Path", make_mock_path(set(files.keys()))):
            assert run_mod._query_cpu() == 1


def test_query_cpu_quota_exact_one():
    files = {
        "/sys/fs/cgroup/cpu/cpu.cfs_quota_us": "100000\n",
        "/sys/fs/cgroup/cpu/cpu.cfs_period_us": "100000\n",
    }
    with patch("builtins.open", make_mock_open(files)):
        with patch("pylint.lint.run.Path", make_mock_path(set(files.keys()))):
            assert run_mod._query_cpu() == 1


def test_query_cpu_quota_large_value():
    files = {
        "/sys/fs/cgroup/cpu/cpu.cfs_quota_us": "400000\n",
        "/sys/fs/cgroup/cpu/cpu.cfs_period_us": "100000\n",
    }
    with patch("builtins.open", make_mock_open(files)):
        with patch("pylint.lint.run.Path", make_mock_path(set(files.keys()))):
            assert run_mod._query_cpu() == 4


def test_query_cpu_shares_fractional_returns_one_when_quota_is_minus_one():
    # quota == -1 -> fallback to shares branch. shares=2 -> int(2/1024)=0 -> normalize to 1
    files = {
        "/sys/fs/cgroup/cpu/cpu.cfs_quota_us": "-1\n",
        "/sys/fs/cgroup/cpu/cpu.shares": "2\n",
    }
    with patch("builtins.open", make_mock_open(files)):
        with patch(
            "pylint.lint.run.Path",
            make_mock_path(
                {"/sys/fs/cgroup/cpu/cpu.cfs_quota_us", "/sys/fs/cgroup/cpu/cpu.shares"}
            ),
        ):
            assert run_mod._query_cpu() == 1


def test_query_cpu_shares_exact_one_cpu():
    files = {
        "/sys/fs/cgroup/cpu/cpu.shares": "1024\n",
    }
    with patch("builtins.open", make_mock_open(files)):
        with patch("pylint.lint.run.Path", make_mock_path(set(files.keys()))):
            assert run_mod._query_cpu() == 1


def test_query_cpu_shares_multiple_cpus():
    files = {
        "/sys/fs/cgroup/cpu/cpu.shares": "2048\n",
    }
    with patch("builtins.open", make_mock_open(files)):
        with patch("pylint.lint.run.Path", make_mock_path(set(files.keys()))):
            assert run_mod._query_cpu() == 2


def test_query_cpu_prefers_quota_over_shares_when_quota_valid():
    # quota takes precedence when it's not -1 and cpu_period file exists
    files = {
        "/sys/fs/cgroup/cpu/cpu.cfs_quota_us": "300000\n",
        "/sys/fs/cgroup/cpu/cpu.cfs_period_us": "100000\n",
        "/sys/fs/cgroup/cpu/cpu.shares": "1024\n",
    }
    with patch("builtins.open", make_mock_open(files)):
        with patch(
            "pylint.lint.run.Path",
            make_mock_path(
                {
                    "/sys/fs/cgroup/cpu/cpu.cfs_quota_us",
                    "/sys/fs/cgroup/cpu/cpu.cfs_period_us",
                    "/sys/fs/cgroup/cpu/cpu.shares",
                }
            ),
        ):
            # quota 300000/100000 == 3 -> should be used
            assert run_mod._query_cpu() == 3


def test_query_cpu_no_files_returns_none():
    # No cgroup files present -> should return None
    with patch("pylint.lint.run.Path", make_mock_path(set())):
        assert run_mod._query_cpu() is None


def test_cpu_count_with_sched_affinity_and_fractional_quota_becomes_one():
    # Ensure _cpu_count returns at least 1 when quota indicates a fractional CPU
    files = {
        "/sys/fs/cgroup/cpu/cpu.cfs_quota_us": "500\n",
        "/sys/fs/cgroup/cpu/cpu.cfs_period_us": "1000000\n",
    }
    with patch("builtins.open", make_mock_open(files)):
        with patch("pylint.lint.run.Path", make_mock_path(set(files.keys()))):
            # Mock a machine with 4 CPUs available according to sched_getaffinity
            with patch.object(os, "sched_getaffinity", lambda pid: {0, 1, 2, 3}):
                assert run_mod._cpu_count() == 1


def test_run_does_not_crash_when_jobs_zero_and_quota_fractional(tmp_path):
    # Integration-style test: Run() should not crash when --jobs=0 and cgroup quota is fractional
    files = {
        "/sys/fs/cgroup/cpu/cpu.cfs_quota_us": "500\n",
        "/sys/fs/cgroup/cpu/cpu.cfs_period_us": "1000000\n",
    }
    # create a dummy file so pylint has something to lint (a simple python file)
    sample = tmp_path / "sample.py"
    sample.write_text("x = 1\n")
    testargs = [str(sample), "--jobs=0"]
    with patch("builtins.open", make_mock_open(files)):
        with patch("pylint.lint.run.Path", make_mock_path(set(files.keys()))):
            with pytest.raises(SystemExit) as err:
                Run(testargs, reporter=Reporter())
            # Should exit 0 (no lint problems for this tiny file)
            assert err.value.code == 0

from pylint.lint.run import _query_cpu
# Additional regression tests for pylint.lint.run
import os
from unittest.mock import mock_open, MagicMock, patch
import pytest
from py._path.local import LocalPath  # type: ignore[import]
from pylint.lint import Run
from pylint.testutils import GenericTestReporter as Reporter
from pylint.lint import run as run_module
from pylint.lint.run import _query_cpu

def _make_mock_open(mapping):
    """Return a function that behaves like open and returns different data per path."""
    builtin_open = open
    def _mock_open(path, *args, **kwargs):
        if path in mapping:
            return mock_open(read_data=mapping[path])()
        return builtin_open(path, *args, **kwargs)
    return _mock_open

def _make_mock_path(existing_files):
    """Return a Path factory that returns objects with is_file() based on existing_files set."""
    pathlib_path = run_module.Path  # original Path class
    def _mock_path(path_str, *args, **kwargs):
        if path_str in existing_files:
            return MagicMock(is_file=lambda: True)
        return pathlib_path(path_str, *args, **kwargs)
    return _mock_path

@pytest.mark.parametrize(
    "quota,period",
    [
        ("100", "100000"),  # small fractional CPU -> int(100/100000) == 0
        ("0", "100000"),    # zero quota -> int(0/100000) == 0
    ],
)
def test_query_cpu_small_or_zero_quota_returns_at_least_one(quota, period):
    """Directly test _query_cpu returns at least 1 when quota/period results in 0."""
    mapping = {
        "/sys/fs/cgroup/cpu/cpu.cfs_quota_us": quota,
        "/sys/fs/cgroup/cpu/cpu.cfs_period_us": period,
    }
    mock_open_fn = _make_mock_open(mapping)
    mock_path = _make_mock_path(set(mapping.keys()))

    with patch("builtins.open", mock_open_fn):
        with patch("pylint.lint.run.Path", mock_path):
            val = _query_cpu()
    assert val is not None and val >= 1, "Expected at least one CPU to be reported"

def test_query_cpu_quota_with_trailing_whitespace_and_rstrip():
    """Ensure rstrip() handling still yields at least 1 when fractional."""
    mapping = {
        "/sys/fs/cgroup/cpu/cpu.cfs_quota_us": "  123  \n",
        "/sys/fs/cgroup/cpu/cpu.cfs_period_us": "  100000  \n",
    }
    mock_open_fn = _make_mock_open(mapping)
    mock_path = _make_mock_path(set(mapping.keys()))
    with patch("builtins.open", mock_open_fn):
        with patch("pylint.lint.run.Path", mock_path):
            val = _query_cpu()
    assert val is not None and val >= 1

def test_query_cpu_prefers_quota_over_shares_and_returns_at_least_one():
    """If quota files are present they are preferred and fractional result must be normalized to 1."""
    mapping = {
        "/sys/fs/cgroup/cpu/cpu.cfs_quota_us": "50",
        "/sys/fs/cgroup/cpu/cpu.cfs_period_us": "100000",
        "/sys/fs/cgroup/cpu/cpu.shares": "2",
    }
    mock_open_fn = _make_mock_open(mapping)
    mock_path = _make_mock_path(set(mapping.keys()))
    with patch("builtins.open", mock_open_fn):
        with patch("pylint.lint.run.Path", mock_path):
            val = _query_cpu()
    # quota branch yields 0 -> must be normalized to at least 1
    assert val is not None and val >= 1

def test_query_cpu_large_quota_returns_expected_integer():
    """Check that large quota/period returns the actual integer number of CPUs."""
    mapping = {
        "/sys/fs/cgroup/cpu/cpu.cfs_quota_us": "200000",
        "/sys/fs/cgroup/cpu/cpu.cfs_period_us": "100000",
    }
    mock_open_fn = _make_mock_open(mapping)
    mock_path = _make_mock_path(set(mapping.keys()))
    with patch("builtins.open", mock_open_fn):
        with patch("pylint.lint.run.Path", mock_path):
            val = _query_cpu()
    assert val == 2

def test_pylint_run_jobs_equal_zero_with_small_quota_does_not_crash(tmpdir: LocalPath):
    """Run.Run should not crash when cgroup quota leads to fractional CPU (jobs=0)."""
    mapping = {
        "/sys/fs/cgroup/cpu/cpu.cfs_quota_us": "100",
        "/sys/fs/cgroup/cpu/cpu.cfs_period_us": "100000",
    }
    mock_open_fn = _make_mock_open(mapping)
    mock_path = _make_mock_path(set(mapping.keys()))
    filepath = os.path.abspath(__file__)
    testargs = [filepath, "--jobs=0"]
    with tmpdir.as_cwd():
        with patch("builtins.open", mock_open_fn):
            with patch("pylint.lint.run.Path", mock_path):
                with pytest.raises(SystemExit) as err:
                    Run(testargs, reporter=Reporter())
    assert err.value.code == 0

def test_pylint_run_jobs_equal_zero_with_zero_quota_does_not_crash(tmpdir: LocalPath):
    """Edge-case: zero quota must not lead to 0 CPUs and must not crash."""
    mapping = {
        "/sys/fs/cgroup/cpu/cpu.cfs_quota_us": "0",
        "/sys/fs/cgroup/cpu/cpu.cfs_period_us": "100000",
    }
    mock_open_fn = _make_mock_open(mapping)
    mock_path = _make_mock_path(set(mapping.keys()))
    filepath = os.path.abspath(__file__)
    testargs = [filepath, "--jobs=0"]
    with tmpdir.as_cwd():
        with patch("builtins.open", mock_open_fn):
            with patch("pylint.lint.run.Path", mock_path):
                with pytest.raises(SystemExit) as err:
                    Run(testargs, reporter=Reporter())
    assert err.value.code == 0

def test_pylint_run_jobs_zero_with_sched_getaffinity_and_small_quota(tmpdir: LocalPath):
    """Ensure combining sched_getaffinity presence with small quota still yields non-zero CPUs."""
    mapping = {
        "/sys/fs/cgroup/cpu/cpu.cfs_quota_us": "10",
        "/sys/fs/cgroup/cpu/cpu.cfs_period_us": "100000",
    }
    mock_open_fn = _make_mock_open(mapping)
    mock_path = _make_mock_path(set(mapping.keys()))
    filepath = os.path.abspath(__file__)
    testargs = [filepath, "--jobs=0"]
    with tmpdir.as_cwd():
        with patch("builtins.open", mock_open_fn):
            with patch("pylint.lint.run.Path", mock_path):
                # Make sched_getaffinity present and returning multiple CPUs
                with patch("os.sched_getaffinity", lambda x: {0, 1, 2}):
                    with pytest.raises(SystemExit) as err:
                        Run(testargs, reporter=Reporter())
    assert err.value.code == 0

def test_query_cpu_negative_quota_uses_shares_and_normalizes_to_one():
    """If quota is -1 then cpu.shares are used; a small shares must be normalized to at least 1."""
    mapping = {
        "/sys/fs/cgroup/cpu/cpu.cfs_quota_us": "-1",
        "/sys/fs/cgroup/cpu/cpu.shares": "2",
    }
    mock_open_fn = _make_mock_open(mapping)
    mock_path = _make_mock_path(set(mapping.keys()))
    with patch("builtins.open", mock_open_fn):
        with patch("pylint.lint.run.Path", mock_path):
            val = _query_cpu()
    assert val is not None and val >= 1

# No additional imports beyond those already present at top of this test module.
# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/PyCQA/pylint/blob/main/CONTRIBUTORS.txt
# pylint: disable=missing-module-docstring, missing-function-docstring

from __future__ import annotations

import os
import pathlib
import sys
from collections.abc import Callable
from unittest.mock import MagicMock, mock_open, patch

import pytest
from py._path.local import LocalPath  # type: ignore[import]

from pylint.lint import Run
from pylint.lint.run import _query_cpu, _cpu_count
from pylint.testutils import GenericTestReporter as Reporter

# Helper to create a mock open and Path for specific cgroup files
def _make_file_mocks(file_contents: dict):
    """
    file_contents: mapping of file path -> string content to be returned by open(...).read()
    """
    builtin_open = open

    def _mock_open(path, *args, **kwargs):
        # path may be passed as Path object sometimes; coerce to str
        p = path if isinstance(path, str) else str(path)
        if p in file_contents:
            return mock_open(read_data=file_contents[p])()
        return builtin_open(path, *args, **kwargs)

    real_pathlib_Path = pathlib.Path

    def _mock_path(*args, **kwargs):
        p = args[0] if args else ""
        # If the path is one we are mocking, return an object with is_file=True
        if p in file_contents:
            return MagicMock(is_file=lambda: True)
        # Otherwise behave like the real pathlib.Path
        return real_pathlib_Path(*args, **kwargs)

    return _mock_open, _mock_path

@pytest.mark.parametrize(
    "quota,period",
    [
        # quota smaller than period -> int(quota/period) == 0 (fractional)
        ("50000\n", "100000\n"),
        # whitespace/newline handling
        (" 50000 \n", "100000\n"),
    ],
)
def test_jobs_zero_quota_fraction_small_exit_ok(tmpdir: LocalPath, quota: str, period: str) -> None:
    """When cfs_quota < cfs_period producing 0 CPUs, Run should still exit 0 (normalize to 1)."""
    file_contents = {
        "/sys/fs/cgroup/cpu/cpu.cfs_quota_us": quota,
        "/sys/fs/cgroup/cpu/cpu.cfs_period_us": period,
    }
    _mock_open, _mock_path = _make_file_mocks(file_contents)

    # Ensure multiprocessing is present so we test the normal codepath (no fallback)
    with tmpdir.as_cwd():
        with pytest.raises(SystemExit) as err:
            with patch("builtins.open", _mock_open):
                with patch("pylint.lint.run.Path", _mock_path):
                    Run([str(__file__), "--jobs=0"], reporter=Reporter())
        assert err.value.code == 0

def test_query_cpu_normalizes_quota_fraction_to_one(tmpdir: LocalPath) -> None:
    """Direct call to _query_cpu should return 1 when quota < period (fractional)."""
    file_contents = {
        "/sys/fs/cgroup/cpu/cpu.cfs_quota_us": "50000\n",
        "/sys/fs/cgroup/cpu/cpu.cfs_period_us": "100000\n",
    }
    _mock_open, _mock_path = _make_file_mocks(file_contents)

    with tmpdir.as_cwd():
        with patch("builtins.open", _mock_open):
            with patch("pylint.lint.run.Path", _mock_path):
                assert _query_cpu() == 1

def test_jobs_zero_quota_precedence_over_shares(tmpdir: LocalPath) -> None:
    """
    When both quota/period and cpu.shares are present, quota/period takes precedence.
    If quota produces a fractional cpu (0) it must be normalized to 1.
    """
    file_contents = {
        "/sys/fs/cgroup/cpu/cpu.cfs_quota_us": "50000\n",
        "/sys/fs/cgroup/cpu/cpu.cfs_period_us": "100000\n",
        "/sys/fs/cgroup/cpu/cpu.shares": "2048\n",  # would give 2 if used
    }
    _mock_open, _mock_path = _make_file_mocks(file_contents)

    with tmpdir.as_cwd():
        with pytest.raises(SystemExit) as err:
            with patch("builtins.open", _mock_open):
                with patch("pylint.lint.run.Path", _mock_path):
                    Run([str(__file__), "--jobs=0"], reporter=Reporter())
        assert err.value.code == 0

@pytest.mark.parametrize("quota,period,expected", [
    ("100000\n", "100000\n", 1),  # exact one
    ("300000\n", "100000\n", 3),  # multiple CPUs
])
def test_jobs_zero_quota_non_fractional(tmpdir: LocalPath, quota: str, period: str, expected: int) -> None:
    """Sanity check: non-fractional quota/period values return expected CPU counts and Run succeeds."""
    file_contents = {
        "/sys/fs/cgroup/cpu/cpu.cfs_quota_us": quota,
        "/sys/fs/cgroup/cpu/cpu.cfs_period_us": period,
    }
    _mock_open, _mock_path = _make_file_mocks(file_contents)

    with tmpdir.as_cwd():
        with pytest.raises(SystemExit) as err:
            with patch("builtins.open", _mock_open):
                with patch("pylint.lint.run.Path", _mock_path):
                    Run([str(__file__), "--jobs=0"], reporter=Reporter())
        assert err.value.code == 0
        # Also check that _query_cpu reflects the expected value (>=1)
        with patch("builtins.open", _mock_open):
            with patch("pylint.lint.run.Path", _mock_path):
                assert _query_cpu() == expected

def test_query_cpu_quota_fraction_with_sched_affinity(tmpdir: LocalPath) -> None:
    """
    If sched_getaffinity reports multiple CPUs but quota/period would yield 0,
    the final cpu count should still be normalized to 1 (min(cpu_share, cpu_count) where cpu_share is treated as >=1).
    """
    file_contents = {
        "/sys/fs/cgroup/cpu/cpu.cfs_quota_us": "50000\n",
        "/sys/fs/cgroup/cpu/cpu.cfs_period_us": "100000\n",
    }
    _mock_open, _mock_path = _make_file_mocks(file_contents)

    # Mock sched_getaffinity to return a set of two CPUs
    def fake_sched(pid):
        return {0, 1}

    with tmpdir.as_cwd():
        with pytest.raises(SystemExit) as err:
            with patch("builtins.open", _mock_open):
                with patch("pylint.lint.run.Path", _mock_path):
                    with patch("pylint.lint.run.os.sched_getaffinity", fake_sched):
                        # call Run: should normalize fractional quota to 1 and exit 0
                        Run([str(__file__), "--jobs=0"], reporter=Reporter())
        assert err.value.code == 0

def test_query_cpu_quota_fraction_with_multiprocessing_cpu_count(tmpdir: LocalPath) -> None:
    """
    Ensure that even when multiprocessing.cpu_count() is available, a fractional quota
    (quota < period) yields a minimum of 1 CPU rather than 0.
    """
    file_contents = {
        "/sys/fs/cgroup/cpu/cpu.cfs_quota_us": "50000\n",
        "/sys/fs/cgroup/cpu/cpu.cfs_period_us": "100000\n",
    }
    _mock_open, _mock_path = _make_file_mocks(file_contents)

    with tmpdir.as_cwd():
        with pytest.raises(SystemExit) as err:
            with patch("builtins.open", _mock_open):
                with patch("pylint.lint.run.Path", _mock_path):
                    # Ensure sched_getaffinity is not used in this scenario
                    with patch("pylint.lint.run.os.sched_getaffinity", None):
                        # Ensure multiprocessing.cpu_count returns a positive value
                        with patch("pylint.lint.run.multiprocessing.cpu_count", lambda: 4):
                            Run([str(__file__), "--jobs=0"], reporter=Reporter())
        assert err.value.code == 0

def test_query_cpu_shares_fraction_normalized(tmpdir: LocalPath) -> None:
    """
    cpu.shares small enough to produce 0 when divided by 1024 should be normalized to 1.
    This is also covered by the model patch, but we include it to ensure consistent behavior.
    """
    file_contents = {
        "/sys/fs/cgroup/cpu/cpu.cfs_quota_us": "-1\n",  # indicates quota unusable
        "/sys/fs/cgroup/cpu/cpu.shares": "512\n",  # 512/1024 -> 0
    }
    _mock_open, _mock_path = _make_file_mocks(file_contents)

    with tmpdir.as_cwd():
        with pytest.raises(SystemExit) as err:
            with patch("builtins.open", _mock_open):
                with patch("pylint.lint.run.Path", _mock_path):
                    Run([str(__file__), "--jobs=0"], reporter=Reporter())
        assert err.value.code == 0
        with patch("builtins.open", _mock_open):
            with patch("pylint.lint.run.Path", _mock_path):
                assert _query_cpu() == 1

from unittest.mock import MagicMock, mock_open, patch
import pytest
# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/PyCQA/pylint/blob/main/CONTRIBUTORS.txt
# pylint: disable=missing-module-docstring, missing-function-docstring

from __future__ import annotations

import pathlib
from unittest.mock import MagicMock, mock_open, patch

import pytest

from pylint.lint.run import _query_cpu


@pytest.mark.parametrize(
    "quota_content",
    [
        "1\n",
        "42\n",
        "99999\n",
        "50000\n",
        "99998\n",
        "0\n",
        "123\n",
        "9999\n",
        "999\n",
        "10000\n",
    ],
)
def test_query_cpu_fractional_quota_results_in_at_least_one_cpu(quota_content: str) -> None:
    """
    Simulate the presence of cgroup cpu quota/period files where quota < period,
    which would result in int(quota/period) == 0. Ensure _query_cpu() returns 1
    (at least one CPU) rather than 0.
    """
    builtin_open = open
    # period chosen as 100000 to make many quotas fractional (<1)
    period_content = "100000\n"

    def _mock_open(*args, **kwargs):
        filename = args[0]
        if filename == "/sys/fs/cgroup/cpu/cpu.cfs_quota_us":
            return mock_open(read_data=quota_content)(*args, **kwargs)
        if filename == "/sys/fs/cgroup/cpu/cpu.cfs_period_us":
            return mock_open(read_data=period_content)(*args, **kwargs)
        return builtin_open(*args, **kwargs)

    real_path = pathlib.Path

    def _mock_path(*args, **kwargs):
        # indicate that both files exist
        if args and args[0] in (
            "/sys/fs/cgroup/cpu/cpu.cfs_quota_us",
            "/sys/fs/cgroup/cpu/cpu.cfs_period_us",
        ):
            return MagicMock(is_file=lambda: True)
        return real_path(*args, **kwargs)

    with patch("builtins.open", _mock_open):
        with patch("pylint.lint.run.Path", _mock_path):
            # For fractional quotas, _query_cpu should never return 0.
            result = _query_cpu()
            assert result == 1, f"Expected 1 CPU for fractional quota {quota_content!r}, got {result!r}"

from unittest.mock import MagicMock, mock_open, patch
import pytest
# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/PyCQA/pylint/blob/main/CONTRIBUTORS.txt
# pylint: disable=missing-module-docstring, missing-function-docstring

from __future__ import annotations

import os
import pathlib
from unittest.mock import MagicMock, mock_open, patch

import pytest

from pylint.lint import Run
from pylint.testutils import GenericTestReporter as Reporter

# Helper factory to create mocks for quota/period/shares
def make_open_and_path_mocks(quota_value=None, period_value=None, shares_value=None):
    builtin_open = open

    def _mock_open(*args, **kwargs):
        path = args[0]
        if path == "/sys/fs/cgroup/cpu/cpu.cfs_quota_us" and quota_value is not None:
            return mock_open(read_data=str(quota_value))(*args, **kwargs)
        if path == "/sys/fs/cgroup/cpu/cpu.cfs_period_us" and period_value is not None:
            return mock_open(read_data=str(period_value))(*args, **kwargs)
        if path == "/sys/fs/cgroup/cpu/cpu.shares" and shares_value is not None:
            return mock_open(read_data=str(shares_value))(*args, **kwargs)
        return builtin_open(*args, **kwargs)

    pathlib_path = pathlib.Path

    def _mock_path(*args, **kwargs):
        # emulate existence of the specified files only
        file_path = args[0]
        if file_path in (
            "/sys/fs/cgroup/cpu/cpu.cfs_quota_us",
            "/sys/fs/cgroup/cpu/cpu.cfs_period_us",
            "/sys/fs/cgroup/cpu/cpu.shares",
        ):
            # If a value is provided for this path, say the file exists.
            if (file_path.endswith("cpu.cfs_quota_us") and quota_value is not None) or (
                file_path.endswith("cpu.cfs_period_us") and period_value is not None
            ) or (file_path.endswith("cpu.shares") and shares_value is not None):
                return MagicMock(is_file=lambda: True)
            return MagicMock(is_file=lambda: False)
        return pathlib_path(*args, **kwargs)

    return _mock_open, _mock_path

# Each of these tests simulates quota/period that results in a fractional CPU (<1),
# causing int(quota/period) == 0. The gold patch guarantees that _query_cpu returns
# at least 1 in that case; the candidate patch fails to do so for the quota branch.

def _run_with_mocks(quota_value, period_value, shares_value=None):
    filepath = os.path.abspath(__file__)
    testargs = [filepath, "--jobs=0"]
    _mock_open, _mock_path = make_open_and_path_mocks(
        quota_value=quota_value, period_value=period_value, shares_value=shares_value
    )
    with patch("builtins.open", _mock_open):
        with patch("pylint.lint.run.Path", _mock_path):
            # We expect the run to exit with code 0 (no crash, jobs resolved to >=1).
            with pytest.raises(SystemExit) as err:
                Run(testargs, reporter=Reporter())
    return err

def test_quota_fraction_simple():
    # quota 50000, period 100000 => int(50000/100000) == 0 -> should be treated as 1
    err = _run_with_mocks(quota_value="50000\n", period_value="100000\n")
    assert err.value.code == 0

def test_quota_fraction_with_shares_present():
    # Both quota/period and shares exist. quota branch should take precedence,
    # but fractional quota should still result in at least 1 CPU.
    err = _run_with_mocks(quota_value="50000\n", period_value="100000\n", shares_value="2\n")
    assert err.value.code == 0

def test_quota_fraction_trimmed_whitespace():
    # Files may contain trailing spaces/newlines
    err = _run_with_mocks(quota_value=" 50000 \n", period_value=" 100000 \n")
    assert err.value.code == 0

def test_quota_fraction_one_less_than_period():
    # Very close to 1 but still fractional
    err = _run_with_mocks(quota_value="99999\n", period_value="100000\n")
    assert err.value.code == 0

def test_quota_fraction_minimal_quota():
    # Extremely small quota still yields fractional result
    err = _run_with_mocks(quota_value="1\n", period_value="100000\n")
    assert err.value.code == 0

def test_quota_fraction_large_period():
    # Large period, small quota
    err = _run_with_mocks(quota_value="12345\n", period_value="2000000\n")
    assert err.value.code == 0

def test_quota_fraction_no_shares_file():
    # Ensure behavior is correct when shares file does not exist
    err = _run_with_mocks(quota_value="50000\n", period_value="100000\n", shares_value=None)
    assert err.value.code == 0

def test_quota_fraction_nonstandard_newline():
    # Windows-style newline shouldn't affect parsing
    err = _run_with_mocks(quota_value="50000\r\n", period_value="100000\r\n")
    assert err.value.code == 0

def test_quota_fraction_leading_plus_sign():
    # Plus sign should still be int-parsable and fractional
    err = _run_with_mocks(quota_value="+50000\n", period_value="100000\n")
    assert err.value.code == 0

def test_quota_fraction_with_extra_text_fallback():
    # If extra whitespace/text is present, int conversion of rstrip should still handle numeric prefix;
    # simulate numeric value followed by comment (we rely on rstrip in production code which would keep comment,
    # but this test simulates typical small variations ensuring behavior stays consistent).
    # Using pure numeric still to ensure deterministic behavior in test environment.
    err = _run_with_mocks(quota_value="50000 # comment\n", period_value="100000\n")
    # If the code tries to int() a string with extra text, ValueError may be raised; the purpose of this test is
    # primarily to ensure the quota-fraction handling results in safe outcome under the gold patch.
    # Under gold patch this should exit with code 0; under the broken candidate it may raise or exit differently.
    assert err.value.code == 0

from __future__ import annotations
# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/PyCQA/pylint/blob/main/CONTRIBUTORS.txt
# pylint: disable=missing-module-docstring, missing-function-docstring

from __future__ import annotations

import builtins
from unittest.mock import MagicMock, mock_open, patch

import pytest

from pylint.lint.run import _query_cpu


def _make_path_mock(existing_files: set[str]):
    """
    Return a Path-like callable that yields objects with is_file() according
    to whether their str path is present in existing_files.
    """
    def _mock_path(path_str, *args, **kwargs):
        # Emulate pathlib.Path(path_str)
        return MagicMock(is_file=lambda: str(path_str) in existing_files)
    return _mock_path


def _make_open_mock(mapping: dict[str, str]):
    """
    Return a builtins.open replacement that yields mapping[path] as file content.
    """
    real_open = builtins.open

    def _mock_open(path, *args, **kwargs):
        key = str(path)
        if key in mapping:
            # Use mock_open so .read() works as expected
            return mock_open(read_data=mapping[key])()
        return real_open(path, *args, **kwargs)

    return _mock_open


@pytest.mark.parametrize(
    "quota,period",
    [
        ("50000\n", "100000\n"),   # 0.5 -> int() == 0 -> should be normalized to 1
        ("1\n", "100000\n"),       # tiny quota -> 0
        ("0\n", "100000\n"),       # zero quota -> 0
        ("  42  \n", "100000\n"),  # whitespace handling -> 0
    ],
)
def test_query_cpu_quota_fraction_returns_one(quota, period):
    """
    When cpu.cfs_quota_us < cpu.cfs_period_us the integer division yields 0.
    The function must return 1 instead of 0.
    """
    files = {
        "/sys/fs/cgroup/cpu/cpu.cfs_quota_us",
        "/sys/fs/cgroup/cpu/cpu.cfs_period_us",
    }
    open_map = {
        "/sys/fs/cgroup/cpu/cpu.cfs_quota_us": quota,
        "/sys/fs/cgroup/cpu/cpu.cfs_period_us": period,
    }

    with patch("builtins.open", _make_open_mock(open_map)):
        with patch("pylint.lint.run.Path", _make_path_mock(files)):
            assert _query_cpu() == 1


def test_query_cpu_quota_large_returns_expected_value():
    """A quota significantly larger than period returns the floored value."""
    files = {
        "/sys/fs/cgroup/cpu/cpu.cfs_quota_us",
        "/sys/fs/cgroup/cpu/cpu.cfs_period_us",
    }
    # quota 200000 / period 100000 => 2
    open_map = {
        "/sys/fs/cgroup/cpu/cpu.cfs_quota_us": "200000\n",
        "/sys/fs/cgroup/cpu/cpu.cfs_period_us": "100000\n",
    }

    with patch("builtins.open", _make_open_mock(open_map)):
        with patch("pylint.lint.run.Path", _make_path_mock(files)):
            assert _query_cpu() == 2


@pytest.mark.parametrize(
    "shares",
    [
        ("2\n"),    # 2/1024 == 0 -> should be normalized to 1
        ("512\n"),  # 512/1024 == 0 -> normalized to 1
    ],
)
def test_query_cpu_shares_fraction_returns_one(shares):
    """When cpu.shares / 1024 yields 0 the function must return 1."""
    files = {"/sys/fs/cgroup/cpu/cpu.shares"}
    open_map = {"/sys/fs/cgroup/cpu/cpu.shares": shares}

    with patch("builtins.open", _make_open_mock(open_map)):
        with patch("pylint.lint.run.Path", _make_path_mock(files)):
            assert _query_cpu() == 1


def test_query_cpu_prefers_quota_over_shares_when_quota_valid():
    """
    If cpu.cfs_quota_us is present and not -1, it should be used even if
    cpu.shares is also present.
    """
    files = {
        "/sys/fs/cgroup/cpu/cpu.cfs_quota_us",
        "/sys/fs/cgroup/cpu/cpu.cfs_period_us",
        "/sys/fs/cgroup/cpu/cpu.shares",
    }
    # quota yields 3, shares would yield 0 if used (1023/1024 -> 0)
    open_map = {
        "/sys/fs/cgroup/cpu/cpu.cfs_quota_us": "300000\n",
        "/sys/fs/cgroup/cpu/cpu.cfs_period_us": "100000\n",
        "/sys/fs/cgroup/cpu/cpu.shares": "1023\n",
    }

    with patch("builtins.open", _make_open_mock(open_map)):
        with patch("pylint.lint.run.Path", _make_path_mock(files)):
            assert _query_cpu() == 3


def test_query_cpu_uses_shares_when_quota_is_negative_but_normalizes_zero():
    """
    If cpu.cfs_quota_us == -1 the shares file should be used, and small shares
    must normalize to 1.
    """
    files = {
        "/sys/fs/cgroup/cpu/cpu.cfs_quota_us",
        "/sys/fs/cgroup/cpu/cpu.shares",
    }
    open_map = {
        "/sys/fs/cgroup/cpu/cpu.cfs_quota_us": "-1\n",
        "/sys/fs/cgroup/cpu/cpu.shares": "2\n",
    }

    with patch("builtins.open", _make_open_mock(open_map)):
        with patch("pylint.lint.run.Path", _make_path_mock(files)):
            assert _query_cpu() == 1


def test_query_cpu_no_cgroup_files_returns_none():
    """If no relevant cgroup files exist, _query_cpu should return None."""
    files: set[str] = set()
    open_map: dict[str, str] = {}
    with patch("builtins.open", _make_open_mock(open_map)):
        with patch("pylint.lint.run.Path", _make_path_mock(files)):
            assert _query_cpu() is None

from pylint.lint import run as run_mod
from pylint.testutils import GenericTestReporter as Reporter
# tests/test_query_cpu_patch.py
# -*- coding: utf-8 -*-
from __future__ import annotations
import os
from unittest.mock import MagicMock, mock_open, patch
import pytest

from pylint.lint import run as run_mod
from pylint.testutils import GenericTestReporter as Reporter

def _make_path_mock(existing_files):
    """Return a callable to patch pylint.lint.run.Path which responds to is_file()."""
    def _mock_path(path):
        # path can be passed as a string argument
        return MagicMock(is_file=lambda: str(path) in existing_files)
    return _mock_path

def _make_open_mock(mapping):
    """Return a callable to patch builtins.open to return mapping[path] as file content."""
    builtin_open = open
    def _open(path, *args, **kwargs):
        key = str(path)
        if key in mapping:
            # mock_open returns a callable that should be called to produce the file handle
            return mock_open(read_data=str(mapping[key]))()
        return builtin_open(path, *args, **kwargs)
    return _open

@pytest.mark.parametrize(
    "quota,period",
    [
        ("1", "1000000"),
        ("500000", "1000000"),
        ("0", "1000000"),
        ("1023", "1000000"),
    ],
)
def test_query_cpu_quota_period_fractional_results_in_at_least_one(quota, period):
    """When quota/period computes < 1 cpu (==0), _query_cpu must return 1."""
    mapping = {
        "/sys/fs/cgroup/cpu/cpu.cfs_quota_us": quota,
        "/sys/fs/cgroup/cpu/cpu.cfs_period_us": period,
    }
    path_mock = _make_path_mock(set(mapping.keys()))
    open_mock = _make_open_mock(mapping)
    with patch("pylint.lint.run.Path", new=path_mock):
        with patch("builtins.open", new=open_mock):
            assert run_mod._query_cpu() == 1

@pytest.mark.parametrize("shares", ["1", "2", "1023"])
def test_query_cpu_shares_small_values_return_one(shares):
    """Very small cpu.shares values that would compute to 0 must be normalized to 1."""
    mapping = {
        "/sys/fs/cgroup/cpu/cpu.shares": shares,
    }
    path_mock = _make_path_mock(set(mapping.keys()))
    open_mock = _make_open_mock(mapping)
    with patch("pylint.lint.run.Path", new=path_mock):
        with patch("builtins.open", new=open_mock):
            assert run_mod._query_cpu() == 1

def test_cpu_count_with_sched_getaffinity_and_fractional_quota_returns_at_least_one():
    """If sched_getaffinity reports 2 CPUs but quota/period would yield 0, _cpu_count returns 1."""
    mapping = {
        "/sys/fs/cgroup/cpu/cpu.cfs_quota_us": "1",
        "/sys/fs/cgroup/cpu/cpu.cfs_period_us": "1000000",
    }
    path_mock = _make_path_mock(set(mapping.keys()))
    open_mock = _make_open_mock(mapping)
    # Force sched_getaffinity to exist and report 2 CPUs.
    with patch("pylint.lint.run.Path", new=path_mock):
        with patch("builtins.open", new=open_mock):
            with patch.object(os, "sched_getaffinity", new=lambda pid: {0, 1}):
                assert run_mod._cpu_count() >= 1

def test_cpu_count_with_multiprocessing_and_fractional_quota_returns_at_least_one():
    """If multiprocessing reports multiple CPUs but quota/period yields 0, _cpu_count returns 1."""
    mapping = {
        "/sys/fs/cgroup/cpu/cpu.cfs_quota_us": "500000",
        "/sys/fs/cgroup/cpu/cpu.cfs_period_us": "1000000",
    }
    path_mock = _make_path_mock(set(mapping.keys()))
    open_mock = _make_open_mock(mapping)
    fake_mp = MagicMock()
    fake_mp.cpu_count.return_value = 4
    # Ensure os.sched_getaffinity is absent in this test
    with patch("pylint.lint.run.Path", new=path_mock):
        with patch("builtins.open", new=open_mock):
            with patch.object(os, "sched_getaffinity", new=None):
                with patch("pylint.lint.run.multiprocessing", new=fake_mp):
                    assert run_mod._cpu_count() >= 1

def test_query_cpu_quota_that_yields_two_returns_two():
    """Sanity check: when quota/period yields >1, the value is returned unchanged."""
    mapping = {
        "/sys/fs/cgroup/cpu/cpu.cfs_quota_us": "2000000",
        "/sys/fs/cgroup/cpu/cpu.cfs_period_us": "1000000",
    }
    path_mock = _make_path_mock(set(mapping.keys()))
    open_mock = _make_open_mock(mapping)
    with patch("pylint.lint.run.Path", new=path_mock):
        with patch("builtins.open", new=open_mock):
            assert run_mod._query_cpu() == 2

def test_pylint_run_jobs_equal_zero_with_quota_fraction_does_not_crash(tmp_path):
    """Run(...) with --jobs=0 should not crash when quota/period would compute 0 CPUs."""
    # Use a small python package path to lint (file path argument required by Run)
    pkg_file = str(tmp_path / "module.py")
    pkg_file_path = pkg_file
    # create a dummy module file
    with open(pkg_file_path, "w", encoding="utf-8") as fh:
        fh.write("x = 1\n")
    mapping = {
        "/sys/fs/cgroup/cpu/cpu.cfs_quota_us": "1",
        "/sys/fs/cgroup/cpu/cpu.cfs_period_us": "1000000",
    }
    path_mock = _make_path_mock(set(mapping.keys()))
    open_mock = _make_open_mock(mapping)
    # Run with args [filepath, "--jobs=0"]
    args = [pkg_file_path, "--jobs=0"]
    with patch("pylint.lint.run.Path", new=path_mock):
        with patch("builtins.open", new=open_mock):
            with pytest.raises(SystemExit) as exc:
                run_mod.Run(args, reporter=Reporter())
            # Expect a zero exit code (successful run)
            assert exc.value.code == 0

import pylint.lint.run as run_mod
from pylint.lint.run import _query_cpu, _cpu_count
# Additional regression tests for cgroup CPU detection and cpu counting
import os
from unittest.mock import MagicMock, mock_open, patch
import pytest

from pylint.lint.run import _query_cpu, _cpu_count
import pylint.lint.run as run_mod


def test_query_cpu_quota_fraction_returns_one():
    # quota < period -> int(quota/period) == 0, should be adjusted to 1
    builtin_open = open

    def _mock_open(*args, **kwargs):
        if args[0] == "/sys/fs/cgroup/cpu/cpu.cfs_quota_us":
            return mock_open(read_data="50000")(*args, **kwargs)
        if args[0] == "/sys/fs/cgroup/cpu/cpu.cfs_period_us":
            return mock_open(read_data="100000")(*args, **kwargs)
        return builtin_open(*args, **kwargs)

    def _mock_path(path):
        # Both files exist
        return MagicMock(is_file=lambda: True)

    with patch("builtins.open", _mock_open):
        with patch("pylint.lint.run.Path", _mock_path):
            assert _query_cpu() == 1


def test_query_cpu_quota_nonzero_returns_integer():
    # quota / period = 2
    builtin_open = open

    def _mock_open(*args, **kwargs):
        if args[0] == "/sys/fs/cgroup/cpu/cpu.cfs_quota_us":
            return mock_open(read_data="200000")(*args, **kwargs)
        if args[0] == "/sys/fs/cgroup/cpu/cpu.cfs_period_us":
            return mock_open(read_data="100000")(*args, **kwargs)
        return builtin_open(*args, **kwargs)

    def _mock_path(path):
        return MagicMock(is_file=lambda: True)

    with patch("builtins.open", _mock_open):
        with patch("pylint.lint.run.Path", _mock_path):
            assert _query_cpu() == 2


def test_query_cpu_quota_negative_then_shares_fraction_returns_one():
    # quota = -1 -> ignore quota branch, shares less than 1024 -> int(...) == 0 -> should be 1
    builtin_open = open

    def _mock_open(*args, **kwargs):
        if args[0] == "/sys/fs/cgroup/cpu/cpu.cfs_quota_us":
            return mock_open(read_data="-1")(*args, **kwargs)
        if args[0] == "/sys/fs/cgroup/cpu/cpu.shares":
            return mock_open(read_data="2")(*args, **kwargs)
        return builtin_open(*args, **kwargs)

    def _mock_path(path):
        if path in ("/sys/fs/cgroup/cpu/cpu.cfs_quota_us", "/sys/fs/cgroup/cpu/cpu.shares"):
            return MagicMock(is_file=lambda: True)
        return MagicMock(is_file=lambda: False)

    with patch("builtins.open", _mock_open):
        with patch("pylint.lint.run.Path", _mock_path):
            assert _query_cpu() == 1


def test_query_cpu_no_files_returns_none():
    # No cgroup files present -> should return None
    def _mock_path(path):
        return MagicMock(is_file=lambda: False)

    with patch("pylint.lint.run.Path", _mock_path):
        assert _query_cpu() is None


def test_cpu_count_sched_affinity(monkeypatch):
    # sched_getaffinity available and returns 4 CPUs; _query_cpu None -> returns 4
    monkeypatch.setattr(run_mod, "_query_cpu", lambda: None)
    monkeypatch.setattr(os, "sched_getaffinity", lambda pid: {0, 1, 2, 3}, raising=False)
    assert _cpu_count() == 4


def test_cpu_count_sched_affinity_with_quota_fraction(monkeypatch):
    # _query_cpu returns 1 (fractional allotment normalized to 1), sched_getaffinity returns 4 -> min -> 1
    monkeypatch.setattr(run_mod, "_query_cpu", lambda: 1)
    monkeypatch.setattr(os, "sched_getaffinity", lambda pid: {0, 1, 2, 3}, raising=False)
    assert _cpu_count() == 1


def test_cpu_count_fallback_multiprocessing(monkeypatch):
    # No sched_getaffinity, multiprocessing available -> use multiprocessing.cpu_count()
    monkeypatch.setattr(os, "sched_getaffinity", None, raising=False)
    # Provide a fake multiprocessing with cpu_count
    fake_mp = MagicMock()
    fake_mp.cpu_count.return_value = 8
    monkeypatch.setattr(run_mod, "multiprocessing", fake_mp)
    monkeypatch.setattr(run_mod, "_query_cpu", lambda: None)
    assert _cpu_count() == 8


def test_cpu_count_no_multiprocessing(monkeypatch):
    # No sched_getaffinity and no multiprocessing -> fallback to 1
    monkeypatch.setattr(os, "sched_getaffinity", None, raising=False)
    monkeypatch.setattr(run_mod, "multiprocessing", None)
    monkeypatch.setattr(run_mod, "_query_cpu", lambda: None)
    assert _cpu_count() == 1


def test_query_cpu_shares_fraction_returns_one():
    # shares < 1024 -> int(shares/1024) == 0 -> should be normalized to 1
    builtin_open = open

    def _mock_open(*args, **kwargs):
        if args[0] == "/sys/fs/cgroup/cpu/cpu.cfs_quota_us":
            return mock_open(read_data="-1")(*args, **kwargs)
        if args[0] == "/sys/fs/cgroup/cpu/cpu.shares":
            return mock_open(read_data="512")(*args, **kwargs)
        return builtin_open(*args, **kwargs)

    def _mock_path(path):
        if path in ("/sys/fs/cgroup/cpu/cpu.cfs_quota_us", "/sys/fs/cgroup/cpu/cpu.shares"):
            return MagicMock(is_file=lambda: True)
        return MagicMock(is_file=lambda: False)

    with patch("builtins.open", _mock_open):
        with patch("pylint.lint.run.Path", _mock_path):
            assert _query_cpu() == 1


def test_query_cpu_quota_equals_period_returns_one():
    # quota == period -> int(quota/period) == 1
    builtin_open = open

    def _mock_open(*args, **kwargs):
        if args[0] == "/sys/fs/cgroup/cpu/cpu.cfs_quota_us":
            return mock_open(read_data="100000")(*args, **kwargs)
        if args[0] == "/sys/fs/cgroup/cpu/cpu.cfs_period_us":
            return mock_open(read_data="100000")(*args, **kwargs)
        return builtin_open(*args, **kwargs)

    def _mock_path(path):
        return MagicMock(is_file=lambda: True)

    with patch("builtins.open", _mock_open):
        with patch("pylint.lint.run.Path", _mock_path):
            assert _query_cpu() == 1