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