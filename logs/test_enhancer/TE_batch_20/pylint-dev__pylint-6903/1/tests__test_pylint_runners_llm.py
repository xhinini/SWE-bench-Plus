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