from pylint import modify_sys_path
from pylint.testutils.utils import _test_sys_path
# -*- coding: utf-8 -*-
import os
import sys

import pytest

from pylint import modify_sys_path
from pylint.testutils.utils import _test_sys_path


# Helper to create a getcwd that returns different values on successive calls.
def make_fake_getcwd(first: str, second: str):
    it = iter([first, second])

    def fake_getcwd():
        try:
            return next(it)
        except StopIteration:
            # If called more than twice return the last value
            return second

    return fake_getcwd


def set_sys_path_and_env(paths, pythonpath, monkeypatch):
    # Use the context manager from test utilities to avoid affecting global state
    monkeypatch.setenv("PYTHONPATH", pythonpath)
    sys.path = list(paths)


def assert_modify_sys_path_result(initial_paths, pythonpath, fake_getcwd, expected):
    with _test_sys_path():
        # Patch os.getcwd for the duration of modify_sys_path call
        orig_getcwd = os.getcwd
        os.getcwd = fake_getcwd
        try:
            modify_sys_path()
            assert sys.path == expected
        finally:
            # restore original getcwd to be safe for other tests
            os.getcwd = orig_getcwd


def test_regression_pop_twice_when_pythonpath_startswith_colon_and_cwd_changes(monkeypatch):
    # Simulate os.getcwd() returning A first, then B.
    A = "/first_cwd"
    B = "/second_cwd"
    initial = [A, "pkg1", "pkg2", "pkg3"]
    # PYTHONPATH starts with ":" and equals f":{B}" (second cwd)
    pythonpath = f":{B}"
    # Expected behavior from gold patch:
    # - Remove first entry because it equals cwd (A)
    # - Then env startswith ":" and is not equal to f":{A}" -> remove next first entry
    expected = initial[2:]

    monkeypatch.setenv("PYTHONPATH", pythonpath)
    sys.path = list(initial)
    fake_getcwd = make_fake_getcwd(A, B)
    assert_modify_sys_path_result(initial, pythonpath, fake_getcwd, expected)


def test_regression_pop_index_one_when_pythonpath_endswith_colon_and_cwd_changes(monkeypatch):
    A = "/first_cwd"
    B = "/second_cwd"
    # place B at index 2 so that after the first pop it's at index 1
    initial = [A, "pkgX", B, "pkgY", "pkgZ"]
    pythonpath = f"{B}:"
    # Gold: pop(0) -> ['pkgX', B, 'pkgY', 'pkgZ']
    # env endswith ':' and not equal to f"{A}:" -> pop(1) -> ['pkgX', 'pkgY', 'pkgZ']
    expected = [initial[1], initial[3], initial[4]]

    monkeypatch.setenv("PYTHONPATH", pythonpath)
    sys.path = list(initial)
    fake_getcwd = make_fake_getcwd(A, B)
    assert_modify_sys_path_result(initial, pythonpath, fake_getcwd, expected)


def test_regression_with_duplicate_cwds_and_pythonpath_startswith_colon(monkeypatch):
    A = "/first_cwd"
    B = "/second_cwd"
    # duplicates of A at index 0 and 1
    initial = [A, A, "lib1", "lib2"]
    pythonpath = f":{B}"
    # Gold: first pop removes index0 (A) -> [A, 'lib1', 'lib2']
    # second condition true (env startswith ':' and not f":{A}") -> pop(0) again -> ['lib1','lib2']
    expected = initial[2:]

    monkeypatch.setenv("PYTHONPATH", pythonpath)
    sys.path = list(initial)
    fake_getcwd = make_fake_getcwd(A, B)
    assert_modify_sys_path_result(initial, pythonpath, fake_getcwd, expected)


def test_regression_with_cwd_at_second_position_and_pythonpath_endswith_colon(monkeypatch):
    A = "/first_cwd"
    B = "/second_cwd"
    # B is at index 1; after removing A at index0, B will be at index0 and the element at index1 is removed by pop(1)
    initial = [A, B, "third", "fourth"]
    pythonpath = f"{B}:"
    # Gold: pop0 -> [B, 'third', 'fourth']; pop(1) -> [B, 'fourth']
    expected = [initial[1], initial[3]]

    monkeypatch.setenv("PYTHONPATH", pythonpath)
    sys.path = list(initial)
    fake_getcwd = make_fake_getcwd(A, B)
    assert_modify_sys_path_result(initial, pythonpath, fake_getcwd, expected)


def test_regression_when_pythonpath_startswith_colon_and_second_cwd_matches_index_one(monkeypatch):
    A = "/first_cwd"
    B = "/second_cwd"
    initial = [A, B, "x", "y"]
    pythonpath = f":{B}"
    # Gold: pop0 -> [B,'x','y']; then since env startswith ":" and env != f":{A}" -> pop0 -> ['x','y']
    expected = initial[2:]

    monkeypatch.setenv("PYTHONPATH", pythonpath)
    sys.path = list(initial)
    fake_getcwd = make_fake_getcwd(A, B)
    assert_modify_sys_path_result(initial, pythonpath, fake_getcwd, expected)


def test_regression_when_pythonpath_endswith_colon_and_second_cwd_at_index_two(monkeypatch):
    A = "/first_cwd"
    B = "/second_cwd"
    initial = [A, "m", B, "n"]
    pythonpath = f"{B}:"
    # Gold: pop0 -> ['m', B, 'n']; env endswith ":" -> pop(1) removes B -> ['m', 'n']
    expected = [initial[1], initial[3]]

    monkeypatch.setenv("PYTHONPATH", pythonpath)
    sys.path = list(initial)
    fake_getcwd = make_fake_getcwd(A, B)
    assert_modify_sys_path_result(initial, pythonpath, fake_getcwd, expected)


def test_regression_multiple_duplicates_and_pythonpath_startswith_colon(monkeypatch):
    A = "/first_cwd"
    B = "/second_cwd"
    initial = [A, A, B, "p", "q"]
    pythonpath = f":{B}"
    # Gold: pop0 -> [A, B, 'p', 'q']; then env startswith ":" and env != f":{A}" -> pop0 -> [B, 'p', 'q']
    expected = initial[2:]

    monkeypatch.setenv("PYTHONPATH", pythonpath)
    sys.path = list(initial)
    fake_getcwd = make_fake_getcwd(A, B)
    assert_modify_sys_path_result(initial, pythonpath, fake_getcwd, expected)


def test_regression_multiple_duplicates_and_pythonpath_endswith_colon(monkeypatch):
    A = "/first_cwd"
    B = "/second_cwd"
    initial = [A, A, B, "s", "t"]
    pythonpath = f"{B}:"
    # Gold: pop0 -> [A, B, 's', 't']; env endswith ":" -> pop(1) removes B -> [A, 's', 't']
    expected = [initial[1], initial[3], initial[4]]

    monkeypatch.setenv("PYTHONPATH", pythonpath)
    sys.path = list(initial)
    fake_getcwd = make_fake_getcwd(A, B)
    assert_modify_sys_path_result(initial, pythonpath, fake_getcwd, expected)


def test_regression_edge_case_short_sys_path_with_pythonpath_endswith_colon(monkeypatch):
    A = "/first_cwd"
    B = "/second_cwd"
    # Only two elements; ensure indexes line up and second pop behavior is correct
    initial = [A, B]
    pythonpath = f"{B}:"
    # Gold: pop0 -> [B]; then env endswith ":" and not equal f"{A}:" -> trying to pop(1) would be a no-op in
    # the expected test environment because the list has only one element left; however, the intended
    # semantics for the real function are to pop index 1 if present. For the gold behavior we expect
    # the final list to be [] if there was an element at index 1 originally removed by pop(1).
    # Starting with [A, B] -> pop0 -> [B]; pop(1) cannot remove anything (index error avoided by environment),
    # but to reflect the intended gold semantics when there is an index 1 element before the second pop,
    # we consider expected to be [B] here.
    expected = [B]

    monkeypatch.setenv("PYTHONPATH", pythonpath)
    sys.path = list(initial)
    fake_getcwd = make_fake_getcwd(A, B)
    assert_modify_sys_path_result(initial, pythonpath, fake_getcwd, expected)


def test_regression_when_no_second_pop_due_to_matching_pythonpath_and_cwd(monkeypatch):
    # This test demonstrates the situation where the second PYTHONPATH check should not remove
    # an additional entry when env equals f":{cwd_second}" only in the candidate's wrong logic.
    # We assert gold behavior which removes the second entry.
    A = "/first_cwd"
    B = "/second_cwd"
    initial = [A, "alpha", "beta", "gamma"]
    # PYTHONPATH equals f":{B}"
    pythonpath = f":{B}"
    # Gold: pop0 -> ['alpha','beta','gamma']; second condition true -> pop0 -> ['beta','gamma']
    expected = initial[2:]

    monkeypatch.setenv("PYTHONPATH", pythonpath)
    sys.path = list(initial)
    fake_getcwd = make_fake_getcwd(A, B)
    assert_modify_sys_path_result(initial, pythonpath, fake_getcwd, expected)

# No extra top-level imports required beyond those in the test file.
import os
from copy import copy
from unittest.mock import patch

import pytest

from pylint import modify_sys_path
from pylint.testutils.utils import _test_sys_path, _test_environ_pythonpath


@pytest.mark.parametrize(
    "initial_paths, pythonpath_env",
    [
        # 1
        (["/cwd/one", "/usr/lib"], ":/cwd/one"),
        # 2
        (["/cwd/one", "/cwd/one", "/usr/lib"], ":/cwd/one"),
        # 3
        (["", "/usr/lib"], ":/cwd/one"),
        # 4
        ([".", "/usr/lib"], ":/cwd/one"),
        # 5
        (["/cwd/one", "/usr/lib"], "/cwd/one:"),
        # 6
        (["/cwd/one", "/cwd/one", "/usr/lib"], "/cwd/one:"),
        # 7
        (["", "/cwd/one", "/usr/lib"], ":/cwd/one"),
        # 8
        (["/cwd/one", "/custom_pythonpath", "/cwd/one", "/usr/lib"], ":/cwd/one"),
        # 9
        (["/cwd/one", "/custom_pythonpath", "/cwd/one", "/usr/lib"], "/cwd/one:"),
        # 10
        (["/cwd/one", "/cwd/one", "/custom_pythonpath", "/usr/lib"], "/cwd/one:"),
    ],
)
def test_modify_sys_path_consistent_cwd_behavior(initial_paths, pythonpath_env):
    """
    These scenarios mock os.getcwd so that the first call returns "/cwd/one"
    and the second call returns "/cwd/two". The model-generated patch calls
    os.getcwd() twice and can get inconsistent values, leading to popping
    an extra entry from sys.path. The correct (gold) implementation calls
    os.getcwd() once and uses the same value for all comparisons.
    """
    cwd_first = "/cwd/one"
    cwd_second = "/cwd/two"

    # Compute expected result using the golden algorithm semantics:
    def expected_after_modify(paths, env_pythonpath, cwd_value):
        sp = list(paths)
        # First conditional: remove first entry if it's "", ".", or cwd
        if sp and sp[0] in ("", ".", cwd_value):
            sp.pop(0)
        # Recompute env pythonpath handling using the same cwd_value
        if env_pythonpath.startswith(":") and env_pythonpath not in (f":{cwd_value}", ":."):
            if sp:
                sp.pop(0)
        elif env_pythonpath.endswith(":") and env_pythonpath not in (f"{cwd_value}:", ".:"):
            if len(sp) > 1:
                sp.pop(1)
        return sp

    expected = expected_after_modify(initial_paths, pythonpath_env, cwd_first)

    with _test_sys_path():
        # Set a copy to avoid mutating the fixture data accidentally
        sys_paths = copy(initial_paths)
        os_sys_path = sys_paths
        # patch os.getcwd so first call returns cwd_first, second call cwd_second
        with patch("os.getcwd", side_effect=[cwd_first, cwd_second]):
            # Ensure PYTHONPATH is set to the desired value for the test
            with _test_environ_pythonpath(pythonpath_env):
                # set sys.path to our scenario
                import sys as _sys
                _sys.path = list(os_sys_path)
                modify_sys_path()
                assert _sys.path == expected, (
                    "modify_sys_path produced unexpected sys.path for "
                    f"initial={initial_paths!r}, PYTHONPATH={pythonpath_env!r}. "
                    f"Expected {expected!r}, got {_sys.path!r}"
                )

from pylint.testutils.utils import _test_sys_path, _test_environ_pythonpath
# content of tests/test_modify_sys_path_regressions.py
import sys
from copy import copy
from unittest.mock import patch

import pytest

from pylint import modify_sys_path
from pylint.testutils.utils import _test_sys_path, _test_environ_pythonpath


@pytest.mark.parametrize(
    "initial, expected",
    [
        # 1) Do not pop if first entry is a non-special path and PYTHONPATH empty
        (["/do_not_remove", "/usr/lib"], ["/do_not_remove", "/usr/lib"]),
        # 2) Pop if first entry is empty string
        (["", "/usr/lib"], ["/usr/lib"]),
        # 3) Pop if first entry is "."
        ([".", "/usr/lib"], ["/usr/lib"]),
    ],
)
def test_modify_sys_path_basic_cases(initial, expected):
    with _test_sys_path():
        sys.path = copy(initial)
        with _test_environ_pythonpath():
            modify_sys_path()
        assert sys.path == expected


def test_modify_sys_path_pop_cwd_first_entry():
    # 4) If first entry equals cwd it should be removed
    cwd = "/tmp/pylint-cwd"
    initial = [cwd, "/custom", "/other"]
    expected = ["/custom", "/other"]
    with _test_sys_path():
        with patch("pylint.__init__.os.getcwd") as mock_getcwd:
            mock_getcwd.return_value = cwd
            sys.path = copy(initial)
            with _test_environ_pythonpath():
                modify_sys_path()
            assert sys.path == expected


def test_modify_sys_path_env_pythonpath_starting_colon_removes_second_entry_after_cwd():
    # 5) If PYTHONPATH starts with ":" (and not equal to f":{cwd}" or ":."),
    # then after popping first (cwd or empty/dot), the next element should be
    # popped as well (pop(0) again).
    cwd = "/home/user"
    initial = [cwd, "/custom", "/other"]
    # After first pop -> ["/custom", "/other"], then env startswith ":" -> pop(0) -> ["/other"]
    expected = ["/other"]
    with _test_sys_path():
        with patch("pylint.__init__.os.getcwd") as mock_getcwd:
            mock_getcwd.return_value = cwd
            sys.path = copy(initial)
            with _test_environ_pythonpath(":/custom"):
                modify_sys_path()
            assert sys.path == expected


def test_modify_sys_path_do_not_pop_when_env_starts_with_colon_and_equals_colon_cwd():
    # 6) If PYTHONPATH == f":{cwd}" then the special second-pop should NOT occur.
    cwd = "/home/user"
    initial = [cwd, cwd, "/other"]
    # After first pop -> [cwd, "/other"], env_pythonpath == f":{cwd}" so skip pop -> unchanged
    expected = [cwd, "/other"]
    with _test_sys_path():
        with patch("pylint.__init__.os.getcwd") as mock_getcwd:
            mock_getcwd.return_value = cwd
            sys.path = copy(initial)
            with _test_environ_pythonpath(f":{cwd}"):
                modify_sys_path()
            assert sys.path == expected


def test_modify_sys_path_env_pythonpath_endswith_colon_pops_index_1_after_first_pop():
    # 7) If PYTHONPATH ends with ":" (and not equal to f"{cwd}:" or ".:"),
    # then pop(1) should be performed (after the possible first pop).
    initial = ["", "/custom", "/other", "/rest"]
    # After first pop -> ["/custom", "/other", "/rest"], then env endswith ":" -> pop(1) -> ["/custom", "/rest"]
    expected = ["/custom", "/rest"]
    with _test_sys_path():
        sys.path = copy(initial)
        with _test_environ_pythonpath("/custom:"):
            modify_sys_path()
        assert sys.path == expected


def test_modify_sys_path_skip_pop_for_pythonpath_colon_dot():
    # 8) If PYTHONPATH == ":." the second pop (for startswith ":") should be skipped.
    cwd = "/tmp/abc"
    initial = ["", cwd, "/x"]
    # After first pop -> [cwd, "/x"], env_pythonpath == ":." -> skip second pop
    expected = [cwd, "/x"]
    with _test_sys_path():
        with patch("pylint.__init__.os.getcwd") as mock_getcwd:
            mock_getcwd.return_value = cwd
            sys.path = copy(initial)
            with _test_environ_pythonpath(":."):
                modify_sys_path()
            assert sys.path == expected


def test_modify_sys_path_do_not_remove_trailing_cwd_entries():
    # 9) Do not remove cwd entries that are not in the first or second/third positions.
    cwd = "/home/me/project"
    initial = ["/somewhere", "/other", cwd]
    expected = ["/somewhere", "/other", cwd]
    with _test_sys_path():
        with patch("pylint.__init__.os.getcwd") as mock_getcwd:
            mock_getcwd.return_value = cwd
            sys.path = copy(initial)
            with _test_environ_pythonpath():
                modify_sys_path()
            assert sys.path == expected


def test_modify_sys_path_multiple_edge_case_combination():
    # 10) Complex case: starting with "", env_pythonpath endswith ":" but equals ".:" should skip pop(1)
    cwd = "/work"
    initial = ["", cwd, "/custom", "/rest"]
    # After first pop -> [cwd, "/custom", "/rest"], env_pythonpath == ".:" -> skip pop(1) -> unchanged further
    expected = [cwd, "/custom", "/rest"]
    with _test_sys_path():
        with patch("pylint.__init__.os.getcwd") as mock_getcwd:
            mock_getcwd.return_value = cwd
            sys.path = copy(initial)
            with _test_environ_pythonpath(".:"):
                modify_sys_path()
            assert sys.path == expected

# These imports are already present in the main test module, but are listed here
# for clarity if the tests are separated into their own module.
import os
import sys
from copy import copy
from unittest.mock import patch

import pytest

from pylint import modify_sys_path
from pylint.testutils.utils import _test_sys_path, _test_environ_pythonpath
import os
import sys
from copy import copy
from unittest.mock import patch

import pytest

from pylint import modify_sys_path
from pylint.testutils.utils import _test_sys_path, _test_environ_pythonpath

# Reuse a default paths set similar to the existing test suite.
DEFAULT_PATHS = [
    "/usr/local/lib/python39.zip",
    "/usr/local/lib/python3.9",
    "/usr/local/lib/python3.9/lib-dynload",
    "/usr/local/lib/python3.9/site-packages",
]

def _setup_and_run(paths, env_pythonpath, getcwd_side_effect):
    """
    Helper to set sys.path, patch os.getcwd to a side effect list,
    set PYTHONPATH via helper and run modify_sys_path.
    Returns the final sys.path (a copy).
    """
    with _test_sys_path(), patch("os.getcwd") as mock_getcwd:
        mock_getcwd.side_effect = getcwd_side_effect
        sys.path = copy(paths)
        with _test_environ_pythonpath(env_pythonpath):
            modify_sys_path()
        return copy(sys.path)

def test_modify_sys_path_getcwd_changes_startswith_colon_rootpath():
    """
    If os.getcwd() returns different values across calls and PYTHONPATH is
    :{first_cwd}, the gold behavior should only remove the very first sys.path
    entry when it matches the cwd; candidate patch may remove two entries.
    """
    cwd1 = "/firstcwd"
    cwd2 = "/secondcwd"
    paths = [cwd1, *DEFAULT_PATHS]
    final = _setup_and_run(paths, f":{cwd1}", [cwd1, cwd2])
    # Gold: only the first entry removed
    assert final == paths[1:]

def test_modify_sys_path_getcwd_changes_startswith_colon_empty_first_entry():
    """
    When the first sys.path entry is '' and PYTHONPATH is :{cwd1}, the gold
    behavior pops only the first entry; candidate may pop twice.
    """
    cwd1 = "/firstcwd"
    cwd2 = "/secondcwd"
    paths = ["", *DEFAULT_PATHS]
    final = _setup_and_run(paths, f":{cwd1}", [cwd1, cwd2])
    assert final == paths[1:]

def test_modify_sys_path_getcwd_changes_startswith_colon_dot_first_entry():
    """
    When the first sys.path entry is '.' and PYTHONPATH is :{cwd1}, ensure only
    a single pop occurs under the gold behavior.
    """
    cwd1 = "/firstcwd"
    cwd2 = "/secondcwd"
    paths = [".", *DEFAULT_PATHS]
    final = _setup_and_run(paths, f":{cwd1}", [cwd1, cwd2])
    assert final == paths[1:]

def test_modify_sys_path_getcwd_changes_startswith_colon_duplicate_cwd():
    """
    When sys.path starts with two identical cwd entries and PYTHONPATH is :{cwd1},
    gold should remove only the very first entry.
    """
    cwd1 = "/firstcwd"
    cwd2 = "/secondcwd"
    paths = [cwd1, cwd1, *DEFAULT_PATHS]
    final = _setup_and_run(paths, f":{cwd1}", [cwd1, cwd2])
    assert final == paths[1:]

def test_modify_sys_path_getcwd_changes_endswith_colon_rootpath():
    """
    Variant where PYTHONPATH ends with ':' and equals '{cwd1}:'; gold should not
    remove the second element and only remove the first matching cwd entry.
    """
    cwd1 = "/firstcwd"
    cwd2 = "/secondcwd"
    paths = [cwd1, *DEFAULT_PATHS]
    final = _setup_and_run(paths, f"{cwd1}:", [cwd1, cwd2])
    assert final == paths[1:]

def test_modify_sys_path_getcwd_changes_endswith_colon_empty_first_entry():
    """
    Starting with '' as first sys.path element and PYTHONPATH='{cwd1}:' should
    result in only the intended single removal.
    """
    cwd1 = "/firstcwd"
    cwd2 = "/secondcwd"
    paths = ["", cwd1, *DEFAULT_PATHS]
    final = _setup_and_run(paths, f"{cwd1}:", [cwd1, cwd2])
    assert final == paths[1:]

def test_modify_sys_path_getcwd_changes_mismatch_no_initial_pop_but_env_triggers():
    """
    If the first sys.path entry does not equal cwd1 (so first pop should not happen),
    but PYTHONPATH startswith ':' and is not equal to :{cwd1} (based on gold's single
    cwd capture), gold still pops once; candidate may behave differently when getcwd
    values change between calls.
    """
    cwd1 = "/firstcwd"
    cwd2 = "/secondcwd"
    # First entry not equal to cwd1 -> no initial pop expected
    paths = ["/do_not_remove", cwd1, *DEFAULT_PATHS]
    final = _setup_and_run(paths, f":{cwd1}", [cwd1, cwd2])
    # Gold: since first entry didn't match, the startswith branch will pop index 0
    # (removing /do_not_remove)
    assert final == paths[1:]

def test_modify_sys_path_getcwd_changes_env_colon_dot_special_case():
    """
    Ensure that PYTHONPATH=':.' (special-case) does not trigger additional
    removals even when os.getcwd() changes between calls.
    """
    cwd1 = "/firstcwd"
    cwd2 = "/secondcwd"
    paths = [cwd1, *DEFAULT_PATHS]
    final = _setup_and_run(paths, ":.", [cwd1, cwd2])
    # Gold: only initial cwd match triggers a single pop
    assert final == paths[1:]

def test_modify_sys_path_getcwd_changes_env_with_trailing_colon_and_nonmatching():
    """
    Ensure that PYTHONPATH ending with ':' but not equal to '{cwd}:' triggers the
    appropriate single removal under gold behavior.
    """
    cwd1 = "/firstcwd"
    cwd2 = "/secondcwd"
    paths = [cwd1, "/custom_pythonpath", *DEFAULT_PATHS]
    final = _setup_and_run(paths, "/custom_pythonpath:", [cwd1, cwd2])
    # Gold expects that it will remove the second element in this scenario:
    assert final == [paths[1]] + paths[3:]

def test_modify_sys_path_getcwd_changes_env_startswith_colon_nonmatching_but_first_is_empty():
    """
    Combination: first is '' (popped), PYTHONPATH startswith ':' and not equal to :{cwd1},
    ensure gold pops only the correct elements.
    """
    cwd1 = "/firstcwd"
    cwd2 = "/secondcwd"
    paths = ["", cwd1, "/custom_pythonpath", *DEFAULT_PATHS]
    final = _setup_and_run(paths, f":/custom_pythonpath", [cwd1, cwd2])
    # Gold: initial '' popped, then env startswith ':' and not matching f":{cwd1}"
    # so a single further pop removes what became the first entry (cwd1)
    assert final == paths[2:]

# No additional import file required; tests use existing test utilities from pylint.testutils.utils.
# New regression tests for modify_sys_path behavior.
from __future__ import annotations

import sys
from copy import copy
from unittest.mock import patch

from pylint import modify_sys_path
from pylint.testutils.utils import _test_environ_pythonpath, _test_sys_path


def _run_with_env_and_cwd(paths, pythonpath, cwd):
    """Helper to run modify_sys_path with controlled sys.path, PYTHONPATH and cwd."""
    with _test_sys_path(), patch("os.getcwd") as mock_getcwd:
        mock_getcwd.return_value = cwd
        sys.path = copy(paths)
        with _test_environ_pythonpath(pythonpath):
            modify_sys_path()
        return sys.path


def test_no_pop_when_first_path_not_special_and_no_pythonpath():
    cwd = "/tmp/cwd"
    paths = ["/usr/lib", "/custom", "/site-packages"]
    # No PYTHONPATH (empty), first element not in ("", ".", cwd) -> no change
    result = _run_with_env_and_cwd(paths, "", cwd)
    assert result == paths


def test_pop_first_when_first_is_cwd():
    cwd = "/home/user/project"
    paths = [cwd, "/usr/lib", "/site-packages"]
    result = _run_with_env_and_cwd(paths, "", cwd)
    assert result == ["/usr/lib", "/site-packages"]


def test_pop_first_when_first_is_empty_string():
    cwd = "/home/user/project"
    paths = ["", "/usr/lib", "/site-packages"]
    result = _run_with_env_and_cwd(paths, "", cwd)
    assert result == ["/usr/lib", "/site-packages"]


def test_pop_first_when_first_is_dot():
    cwd = "/home/user/project"
    paths = [".", "/usr/lib", "/site-packages"]
    result = _run_with_env_and_cwd(paths, "", cwd)
    assert result == ["/usr/lib", "/site-packages"]


def test_pythonpath_starts_with_colon_removes_first_when_not_special():
    # If PYTHONPATH starts with ":" and is not exactly ":." or f":{cwd}",
    # we should remove the first element even if it wasn't "", ".", or cwd.
    cwd = "/home/user/project"
    paths = ["/do_not_remove", "/custom", "/site-packages"]
    result = _run_with_env_and_cwd(paths, ":/custom_pythonpath", cwd)
    # The first element should have been popped
    assert result == ["/custom", "/site-packages"]


def test_pythonpath_endswith_colon_removes_second_after_initial_pop():
    # When first element is cwd, it should be popped first. If PYTHONPATH endswith ":"
    # and is not exactly f"{cwd}:" or ".:", pop index 1 of the *current* sys.path.
    cwd = "/home/user/project"
    paths = [cwd, "/custom_pythonpath", "p1", "p2"]
    result = _run_with_env_and_cwd(paths, "/custom_pythonpath:", cwd)
    # After initial pop -> ['/custom_pythonpath', 'p1', 'p2']
    # Then pop(1) -> ['/custom_pythonpath', 'p2']
    assert result == ["/custom_pythonpath", "p2"]


def test_pythonpath_starts_with_colon_but_equals_colon_cwd_no_extra_pop():
    cwd = "/home/user/project"
    paths = [cwd, "/usr/lib", "/site-packages"]
    # PYTHONPATH is exactly f":{cwd}" -> should NOT trigger the extra pop
    result = _run_with_env_and_cwd(paths, f":{cwd}", cwd)
    assert result == ["/usr/lib", "/site-packages"]


def test_pythonpath_ends_with_colon_equals_cwd_colon_no_second_pop():
    cwd = "/home/user/project"
    paths = [cwd, "/custom_pythonpath", "p1"]
    # PYTHONPATH is exactly f"{cwd}:" -> should NOT trigger pop(1)
    result = _run_with_env_and_cwd(paths, f"{cwd}:", cwd)
    # Only the initial cwd pop should happen
    assert result == ["/custom_pythonpath", "p1"]


def test_no_change_when_pythonpath_has_no_trailing_or_leading_colon():
    cwd = "/home/user/project"
    paths = ["/do_not_remove", "/custom", "/site-packages"]
    # PYTHONPATH doesn't start or end with ":" -> no change
    result = _run_with_env_and_cwd(paths, "/custom_pythonpath", cwd)
    assert result == paths


def test_do_not_remove_trailing_cwd_entry_in_editable_install():
    # Ensure that when cwd appears later in sys.path (editable install scenario),
    # it is not removed by modify_sys_path.
    cwd = "/home/user/project"
    paths = ["/usr/lib", "/custom", cwd]
    result = _run_with_env_and_cwd(paths, "", cwd)
    assert result == paths

from unittest.mock import patch
from copy import copy
# tests/test_modify_sys_path_regression.py
import os
from copy import copy
from unittest.mock import patch

import pytest

from pylint import modify_sys_path
from pylint.testutils.utils import _test_environ_pythonpath, _test_sys_path

ORIGINAL_CWD = "/original_cwd"
CUSTOM_PY = "/custom_pythonpath"
DEFAULT_PATHS = ["lib1", "lib2"]

@pytest.mark.parametrize(
    "initial_first, env_pythonpath, getcwd_side_effect, expected",
    [
        # 1: sys.path starts with cwd, PYTHONPATH starts with :{custom}
        (ORIGINAL_CWD, f":{CUSTOM_PY}", [ORIGINAL_CWD, CUSTOM_PY], DEFAULT_PATHS),
        # 2: sys.path starts with "", PYTHONPATH starts with :{custom}
        ("", f":{CUSTOM_PY}", [ORIGINAL_CWD, CUSTOM_PY], DEFAULT_PATHS),
        # 3: sys.path starts with ".", PYTHONPATH starts with :{custom}
        (".", f":{CUSTOM_PY}", [ORIGINAL_CWD, CUSTOM_PY], DEFAULT_PATHS),
    ],
)
def test_modify_sys_path_startswith_colon_inconsistent_getcwd(
    initial_first, env_pythonpath, getcwd_side_effect, expected
):
    """
    When PYTHONPATH starts with ':' and os.getcwd() returns different values
    between calls, modify_sys_path should still remove both the working
    directory entry and the next entry (custom pythonpath), producing only the
    default paths. The model patch (calling os.getcwd() twice and using the
    second value in later checks) will fail this scenario.
    """
    with _test_sys_path():
        paths = [initial_first, CUSTOM_PY, *DEFAULT_PATHS]
        # make a copy to compare expected in the form used in the tests above
        sys_path = copy(paths)
        # Ensure there is at least one element before accessing sys.path[0]
        os_getcwd_patch = patch("os.getcwd", side_effect=getcwd_side_effect)
        with os_getcwd_patch:
            sys.path = copy(sys_path)
            with _test_environ_pythonpath(env_pythonpath):
                modify_sys_path()
            assert sys.path == expected

@pytest.mark.parametrize(
    "initial_first, env_pythonpath, getcwd_side_effect, expected",
    [
        # 4: sys.path starts with cwd, PYTHONPATH ends with {custom}:
        (ORIGINAL_CWD, f"{CUSTOM_PY}:", [ORIGINAL_CWD, CUSTOM_PY], [CUSTOM_PY, "lib2"]),
        # 5: sys.path starts with "", PYTHONPATH ends with {custom}:
        ("", f"{CUSTOM_PY}:", [ORIGINAL_CWD, CUSTOM_PY], [CUSTOM_PY, "lib2"]),
    ],
)
def test_modify_sys_path_endswith_colon_inconsistent_getcwd(
    initial_first, env_pythonpath, getcwd_side_effect, expected
):
    """
    When PYTHONPATH ends with ':' and os.getcwd() returns different values
    between calls, modify_sys_path must behave as if cwd was determined only once.
    The model patch may fail to remove the expected element.
    """
    with _test_sys_path():
        paths = [initial_first, CUSTOM_PY, *DEFAULT_PATHS]
        sys_path = copy(paths)
        with patch("os.getcwd", side_effect=getcwd_side_effect):
            sys.path = copy(sys_path)
            with _test_environ_pythonpath(env_pythonpath):
                modify_sys_path()
            assert sys.path == expected

@pytest.mark.parametrize(
    "env_pythonpath, getcwd_side_effect, expected",
    [
        # 6: env PYTHONPATH is :{original_cwd} -> gold should NOT pop the custom entry
        (f":{ORIGINAL_CWD}", [ORIGINAL_CWD, CUSTOM_PY], [CUSTOM_PY, "lib1", "lib2"]),
        # 7: env PYTHONPATH is {original_cwd}: -> gold should NOT remove the second entry
        (f"{ORIGINAL_CWD}:", [ORIGINAL_CWD, CUSTOM_PY], [CUSTOM_PY, "lib1", "lib2"]),
    ],
)
def test_modify_sys_path_no_pop_when_pythonpath_matches_original_cwd(
    env_pythonpath, getcwd_side_effect, expected
):
    """
    If PYTHONPATH explicitly references the original cwd (prefix or suffix),
    modify_sys_path should avoid removing the entry. The model patch may use
    the second os.getcwd() and thus remove entries incorrectly.
    """
    with _test_sys_path():
        paths = [ORIGINAL_CWD, CUSTOM_PY, *DEFAULT_PATHS]
        with patch("os.getcwd", side_effect=getcwd_side_effect):
            sys.path = copy(paths)
            with _test_environ_pythonpath(env_pythonpath):
                modify_sys_path()
            assert sys.path == expected

@pytest.mark.parametrize(
    "initial_first, env_pythonpath, getcwd_side_effect, expected",
    [
        # 8: first path is not cwd, PYTHONPATH starts with :{custom}
        ("/do_not_remove", f":{CUSTOM_PY}", [ORIGINAL_CWD, CUSTOM_PY], [CUSTOM_PY, "lib1", "lib2"]),
        # 9: first path is not cwd, PYTHONPATH ends with {custom}:
        ("/do_not_remove", f"{CUSTOM_PY}:", [ORIGINAL_CWD, CUSTOM_PY], ["/do_not_remove", "lib1", "lib2"]),
    ],
)
def test_modify_sys_path_non_cwd_first_entry_inconsistent_getcwd(
    initial_first, env_pythonpath, getcwd_side_effect, expected
):
    """
    When the first entry is not cwd (e.g. '/do_not_remove') and os.getcwd()
    returns different values between calls, the decisions about popping the
    first or second entries should still match the gold behavior.
    The model patch's second-call-based decision can cause an incorrect result.
    """
    with _test_sys_path():
        paths = [initial_first, CUSTOM_PY, *DEFAULT_PATHS]
        with patch("os.getcwd", side_effect=getcwd_side_effect):
            sys.path = copy(paths)
            with _test_environ_pythonpath(env_pythonpath):
                modify_sys_path()
            assert sys.path == expected

def test_modify_sys_path_double_cwd_entry_inconsistent_getcwd():
    """
    When sys.path contains two cwd entries at the start and env_pythonpath
    starts with ':', the gold code will remove both cwd entries and the next
    entry if appropriate; the model patch (using differing cwd values) may
    leave an extra cwd entry behind.
    """
    with _test_sys_path():
        paths = [ORIGINAL_CWD, ORIGINAL_CWD, CUSTOM_PY, *DEFAULT_PATHS]
        with patch("os.getcwd", side_effect=[ORIGINAL_CWD, CUSTOM_PY]):
            sys.path = copy(paths)
            with _test_environ_pythonpath(f":{CUSTOM_PY}"):
                modify_sys_path()
            # gold: both leading ORIGINAL_CWD entries removed and CUSTOM_PY removed => DEFAULT_PATHS
            assert sys.path == DEFAULT_PATHS

from copy import copy
from unittest.mock import patch
from pylint import modify_sys_path
from pylint.testutils.utils import _test_environ_pythonpath, _test_sys_path
# tests/test_modify_sys_path_extra.py
from copy import copy
from unittest.mock import patch

from pylint import modify_sys_path
from pylint.testutils.utils import _test_environ_pythonpath, _test_sys_path

def _default_paths():
    return [
        "/usr/local/lib/python39.zip",
        "/usr/local/lib/python3.9",
        "/usr/local/lib/python3.9/lib-dynload",
        "/usr/local/lib/python3.9/site-packages",
    ]

def test_remove_cwd_when_first_entry_is_cwd():
    cwd = "/fake/cwd"
    default_paths = _default_paths()
    with _test_sys_path(), patch("os.getcwd") as mock_getcwd:
        mock_getcwd.return_value = cwd
        sys_path = [cwd, *default_paths]
        import sys as _sys

        _sys.path = copy(sys_path)
        with _test_environ_pythonpath():
            modify_sys_path()
        assert _sys.path == sys_path[1:]

def test_remove_empty_string_first_entry():
    cwd = "/another/cwd"
    default_paths = _default_paths()
    with _test_sys_path(), patch("os.getcwd") as mock_getcwd:
        mock_getcwd.return_value = cwd
        sys_path = ["", *default_paths]
        import sys as _sys

        _sys.path = copy(sys_path)
        with _test_environ_pythonpath():
            modify_sys_path()
        assert _sys.path == sys_path[1:]

def test_remove_dot_first_entry():
    cwd = "/my/cwd"
    default_paths = _default_paths()
    with _test_sys_path(), patch("os.getcwd") as mock_getcwd:
        mock_getcwd.return_value = cwd
        sys_path = [".", *default_paths]
        import sys as _sys

        _sys.path = copy(sys_path)
        with _test_environ_pythonpath():
            modify_sys_path()
        assert _sys.path == sys_path[1:]

def test_pop_twice_when_pythonpath_startswith_colon_and_not_equal_to_cwd_colon():
    cwd = "/cwd-x"
    default_paths = _default_paths()
    # initial sys.path: [cwd, "/custom", default_paths...]
    with _test_sys_path(), patch("os.getcwd") as mock_getcwd:
        mock_getcwd.return_value = cwd
        sys_path = [cwd, "/custom", *default_paths]
        import sys as _sys

        _sys.path = copy(sys_path)
        # PYTHONPATH starts with ":" and is not equal to f":{cwd}"
        with _test_environ_pythonpath(":/custom"):
            modify_sys_path()
        # First pop removes cwd, second pop (due to startswith ":") removes "/custom"
        assert _sys.path == default_paths

def test_do_not_pop_second_when_pythonpath_startswith_colon_equal_to_cwd_colon_prefixed():
    cwd = "/cwd-y"
    default_paths = _default_paths()
    with _test_sys_path(), patch("os.getcwd") as mock_getcwd:
        mock_getcwd.return_value = cwd
        sys_path = [cwd, "/custom", *default_paths]
        import sys as _sys

        _sys.path = copy(sys_path)
        # PYTHONPATH is exactly f":{cwd}" -> should not trigger the second removal
        with _test_environ_pythonpath(f":{cwd}"):
            modify_sys_path()
        assert _sys.path == ["/custom", *default_paths]

def test_pop_index_one_when_pythonpath_endswith_colon_and_not_equal_to_cwd_colon():
    cwd = "/cwd-z"
    default_paths = _default_paths()
    with _test_sys_path(), patch("os.getcwd") as mock_getcwd:
        mock_getcwd.return_value = cwd
        sys_path = [cwd, "/custom", *default_paths]
        import sys as _sys

        _sys.path = copy(sys_path)
        # PYTHONPATH ends with ":" and is not equal to f"{cwd}:"
        with _test_environ_pythonpath("/custom:"):
            modify_sys_path()
        # First pop removes cwd -> ['/custom', ...]; then pop(1) removes default_paths[0]
        assert _sys.path == ["/custom", *default_paths[1:]]

def test_do_not_pop_index_one_when_pythonpath_endswith_colon_equal_to_cwd_colon():
    cwd = "/cwd-w"
    default_paths = _default_paths()
    with _test_sys_path(), patch("os.getcwd") as mock_getcwd:
        mock_getcwd.return_value = cwd
        sys_path = [cwd, "/custom", *default_paths]
        import sys as _sys

        _sys.path = copy(sys_path)
        # PYTHONPATH equals f"{cwd}:" so should not remove sys.path[1]
        with _test_environ_pythonpath(f"{cwd}:"):
            modify_sys_path()
        assert _sys.path == ["/custom", *default_paths]

def test_preserve_later_cwd_entries_when_editable_install():
    cwd = "/editable/cwd"
    default_paths = _default_paths()
    # Have cwd twice: at front and at the end (editable install)
    with _test_sys_path(), patch("os.getcwd") as mock_getcwd:
        mock_getcwd.return_value = cwd
        sys_path = [cwd, "/custom", *default_paths, cwd]
        import sys as _sys

        _sys.path = copy(sys_path)
        with _test_environ_pythonpath():
            modify_sys_path()
        # Only the first cwd should be removed; the trailing editable cwd should remain
        assert _sys.path == ["/custom", *default_paths, cwd]

def test_no_change_when_first_entry_not_cwd_empty_or_dot_and_no_pythonpath_trickery():
    cwd = "/irrelevant/cwd"
    default_paths = _default_paths()
    with _test_sys_path(), patch("os.getcwd") as mock_getcwd:
        mock_getcwd.return_value = cwd
        sys_path = ["/do_not_remove", *default_paths]
        import sys as _sys

        _sys.path = copy(sys_path)
        with _test_environ_pythonpath():
            modify_sys_path()
        assert _sys.path == sys_path

from copy import copy
from unittest.mock import patch
import sys
from pylint import modify_sys_path
from pylint.testutils.utils import _test_sys_path, _test_environ_pythonpath
# tests/test_modify_sys_path_extra.py
from copy import copy
from unittest.mock import patch

import sys

from pylint import modify_sys_path
from pylint.testutils.utils import _test_sys_path, _test_environ_pythonpath


DEFAULT_PATHS = [
    "/usr/local/lib/python39.zip",
    "/usr/local/lib/python3.9",
    "/usr/local/lib/python3.9/lib-dynload",
    "/usr/local/lib/python3.9/site-packages",
]


def _make_paths(firsts):
    """Helper: produce a sys.path list starting with items in `firsts` then DEFAULT_PATHS."""
    return [*firsts, *DEFAULT_PATHS]


def test_remove_cwd_first_entry():
    cwd = "/tmp/mycwd"
    paths = _make_paths([cwd])
    with _test_sys_path():
        with patch("os.getcwd") as mock_getcwd:
            mock_getcwd.return_value = cwd
            sys.path = copy(paths)
            with _test_environ_pythonpath():
                modify_sys_path()
            assert sys.path == paths[1:]


def test_remove_empty_first_entry():
    cwd = "/tmp/anothercwd"
    paths = _make_paths([""])
    with _test_sys_path():
        with patch("os.getcwd") as mock_getcwd:
            mock_getcwd.return_value = cwd
            sys.path = copy(paths)
            with _test_environ_pythonpath():
                modify_sys_path()
            assert sys.path == paths[1:]


def test_do_not_remove_non_matching_first_entry():
    cwd = "/tmp/cwdx"
    paths = _make_paths(["/do_not_remove"])
    with _test_sys_path():
        with patch("os.getcwd") as mock_getcwd:
            mock_getcwd.return_value = cwd
            sys.path = copy(paths)
            with _test_environ_pythonpath():
                modify_sys_path()
            # unchanged because first entry is not "", ".", or cwd
            assert sys.path == paths


def test_pythonpath_colon_prefix_removes_second_entry_when_not_cwd_colon():
    cwd = "/tmp/cwdp"
    # initial sys.path: [cwd, '/custom', ...]
    paths = [cwd, "/custom_pythonpath", *DEFAULT_PATHS]
    with _test_sys_path():
        with patch("os.getcwd") as mock_getcwd:
            mock_getcwd.return_value = cwd
            sys.path = copy(paths)
            # PYTHONPATH begins with ':' and is not ":{cwd}"
            with _test_environ_pythonpath(":/custom_pythonpath"):
                modify_sys_path()
            # first entry removed because it matched cwd,
            # then because PYTHONPATH started with ':' and wasn't :cwd, pop again
            # resulting in leaving only the '/custom_pythonpath' entry removed too.
            assert sys.path == [paths[1]] + paths[3:]


def test_pythonpath_colon_prefix_does_not_remove_when_equals_colon_cwd():
    cwd = "/tmp/cwdeq"
    paths = [cwd, "/custom_pythonpath", *DEFAULT_PATHS]
    with _test_sys_path():
        with patch("os.getcwd") as mock_getcwd:
            mock_getcwd.return_value = cwd
            sys.path = copy(paths)
            # PYTHONPATH is exactly :{cwd} so second-pop should NOT happen
            with _test_environ_pythonpath(f":{cwd}"):
                modify_sys_path()
            assert sys.path == paths[1:]


def test_pythonpath_colon_suffix_removes_index_1_when_not_cwd_colon():
    cwd = "/tmp/cwdsuf"
    paths = [cwd, "/custom_pythonpath", cwd, *DEFAULT_PATHS]
    with _test_sys_path():
        with patch("os.getcwd") as mock_getcwd:
            mock_getcwd.return_value = cwd
            sys.path = copy(paths)
            # PYTHONPATH ends with ':' and is not "{cwd}:"
            with _test_environ_pythonpath("/custom_pythonpath:"):
                modify_sys_path()
            # First cwd popped, then because of trailing colon and not equal "{cwd}:",
            # the element at index 1 (after the first pop) is removed.
            assert sys.path == [paths[1]] + paths[3:]


def test_pythonpath_colon_suffix_does_not_remove_when_equals_cwd_colon():
    cwd = "/tmp/cwd_no_remove"
    paths = [cwd, "/custom_pythonpath", *DEFAULT_PATHS]
    with _test_sys_path():
        with patch("os.getcwd") as mock_getcwd:
            mock_getcwd.return_value = cwd
            sys.path = copy(paths)
            with _test_environ_pythonpath(f"{cwd}:"):
                modify_sys_path()
            # first entry removed because it matched cwd; trailing-colon case should not remove
            assert sys.path == paths[1:]


def test_remove_dot_first_entry():
    cwd = "/tmp/dotcwd"
    paths = _make_paths(["."])
    with _test_sys_path():
        with patch("os.getcwd") as mock_getcwd:
            mock_getcwd.return_value = cwd
            sys.path = copy(paths)
            with _test_environ_pythonpath():
                modify_sys_path()
            assert sys.path == paths[1:]


def test_complex_duplicate_cwd_with_pythonpath_colon_prefix():
    cwd = "/tmp/dup_cwd"
    # sys.path begins with "" then cwd then custom then defaults
    paths = ["", cwd, "/custom", *DEFAULT_PATHS]
    with _test_sys_path():
        with patch("os.getcwd") as mock_getcwd:
            mock_getcwd.return_value = cwd
            sys.path = copy(paths)
            # PYTHONPATH begins with ':' and references /custom
            with _test_environ_pythonpath(":/custom"):
                modify_sys_path()
            # Starting '' should be removed, then because PYTHONPATH starts with ':'
            # and is not :cwd or :., another pop(0) happens which removes cwd.
            assert sys.path == paths[2:]


def test_single_entry_sys_path_not_index_error():
    """Ensure we don't raise when sys.path has only one entry (it may be removed)."""
    cwd = "/tmp/onlycwd"
    paths = [cwd]
    with _test_sys_path():
        with patch("os.getcwd") as mock_getcwd:
            mock_getcwd.return_value = cwd
            sys.path = copy(paths)
            # No PYTHONPATH special handling
            with _test_environ_pythonpath():
                modify_sys_path()
            # First (and only) entry should be removed, leaving empty list
            assert sys.path == []

from pylint import modify_sys_path
from pylint.testutils.utils import _test_sys_path, _test_environ_pythonpath
# tests/test_modify_sys_path_regressions.py
import os
import sys
from unittest.mock import patch

import pytest

from pylint import modify_sys_path
from pylint.testutils.utils import _test_sys_path, _test_environ_pythonpath


def _run_case_and_assert(initial_paths, pythonpath_value, getcwd_first, getcwd_second, expected):
    with _test_sys_path():
        sys.path = list(initial_paths)
        with _test_environ_pythonpath(pythonpath_value):
            with patch("os.getcwd", side_effect=[getcwd_first, getcwd_second]):
                modify_sys_path()
        assert sys.path == expected


# START: tests where PYTHONPATH startswith ":" and equals the first cwd value
def test_modify_sys_path_startswith_first_cwd_when_syspath_starts_with_cwd():
    cwd1 = "/firstcwd"
    cwd2 = "/secondcwd"
    initial = [cwd1, "p1", "p2"]
    # PYTHONPATH is like :/firstcwd
    pyenv = f":{cwd1}"
    # Under the correct implementation only the first element should be popped
    expected = ["p1", "p2"]
    _run_case_and_assert(initial, pyenv, cwd1, cwd2, expected)


def test_modify_sys_path_startswith_first_cwd_when_syspath_starts_with_empty():
    cwd1 = "/firstcwd"
    cwd2 = "/secondcwd"
    initial = ["", "p1", "p2"]
    pyenv = f":{cwd1}"
    expected = ["p1", "p2"]
    _run_case_and_assert(initial, pyenv, cwd1, cwd2, expected)


def test_modify_sys_path_startswith_first_cwd_when_syspath_starts_with_dot():
    cwd1 = "/firstcwd"
    cwd2 = "/secondcwd"
    initial = [".", "p1", "p2"]
    pyenv = f":{cwd1}"
    expected = ["p1", "p2"]
    _run_case_and_assert(initial, pyenv, cwd1, cwd2, expected)


def test_modify_sys_path_startswith_first_cwd_longer_syspath():
    cwd1 = "/firstcwd"
    cwd2 = "/secondcwd"
    initial = [cwd1, "p1", "p2", "p3", "p4"]
    pyenv = f":{cwd1}"
    expected = ["p1", "p2", "p3", "p4"]
    _run_case_and_assert(initial, pyenv, cwd1, cwd2, expected)

def test_modify_sys_path_startswith_first_cwd_when_second_entry_is_cwd_duplicate():
    cwd1 = "/firstcwd"
    cwd2 = "/secondcwd"
    # Duplicate cwd later in path should not affect correct behaviour
    initial = [cwd1, "p1", cwd1, "p2"]
    pyenv = f":{cwd1}"
    expected = ["p1", cwd1, "p2"]
    _run_case_and_assert(initial, pyenv, cwd1, cwd2, expected)

# START: tests where PYTHONPATH endswith ":" and equals the first cwd value
def test_modify_sys_path_endswith_first_cwd_when_syspath_starts_with_cwd():
    cwd1 = "/firstcwd"
    cwd2 = "/secondcwd"
    initial = [cwd1, "p1", "p2"]
    pyenv = f"{cwd1}:"
    expected = ["p1", "p2"]
    _run_case_and_assert(initial, pyenv, cwd1, cwd2, expected)


def test_modify_sys_path_endswith_first_cwd_when_syspath_starts_with_empty():
    cwd1 = "/firstcwd"
    cwd2 = "/secondcwd"
    initial = ["", "p1", "p2"]
    pyenv = f"{cwd1}:"
    expected = ["p1", "p2"]
    _run_case_and_assert(initial, pyenv, cwd1, cwd2, expected)


def test_modify_sys_path_endswith_first_cwd_when_syspath_starts_with_dot():
    cwd1 = "/firstcwd"
    cwd2 = "/secondcwd"
    initial = [".", "p1", "p2"]
    pyenv = f"{cwd1}:"
    expected = ["p1", "p2"]
    _run_case_and_assert(initial, pyenv, cwd1, cwd2, expected)


def test_modify_sys_path_endswith_first_cwd_with_custom_second_entry():
    cwd1 = "/firstcwd"
    cwd2 = "/secondcwd"
    initial = [cwd1, "/custom_pythonpath", "p2", "p3"]
    pyenv = f"{cwd1}:"
    expected = ["/custom_pythonpath", "p2", "p3"]
    _run_case_and_assert(initial, pyenv, cwd1, cwd2, expected)


def test_modify_sys_path_endswith_first_cwd_duplicate_entries():
    cwd1 = "/firstcwd"
    cwd2 = "/secondcwd"
    initial = [cwd1, cwd1, "p1", "p2"]
    pyenv = f"{cwd1}:"
    # Only the first entry should be removed, and the env-based removal should not remove another
    expected = [cwd1, "p1", "p2"]
    _run_case_and_assert(initial, pyenv, cwd1, cwd2, expected)

from pylint.testutils.utils import _test_sys_path, _test_environ_pythonpath
# tests/test_modify_sys_path_regressions.py
import os
import sys
from copy import copy
from unittest.mock import patch

import pytest

from pylint import modify_sys_path
from pylint.testutils.utils import _test_sys_path, _test_environ_pythonpath

@pytest.mark.parametrize(
    "initial_paths, pythonpath, expected",
    [
        # 1) Two cwd entries, PYTHONPATH=":cwd1" -> only first cwd removed
        (["/cwd1", "/cwd1", "p1", "p2"], ":/cwd1", ["/cwd1", "p1", "p2"]),
        # 2) First entry is empty string then cwd, PYTHONPATH=":cwd1" -> only '' removed
        (["", "/cwd1", "p1", "p2"], ":/cwd1", ["/cwd1", "p1", "p2"]),
        # 3) First entry is '.', then cwd, PYTHONPATH=":cwd1" -> only '.' removed
        ([".", "/cwd1", "p1", "p2"], ":/cwd1", ["/cwd1", "p1", "p2"]),
        # 4) First is cwd, second custom, PYTHONPATH=":cwd1" -> only cwd removed
        (["/cwd1", "/custom", "p1", "p2"], ":/cwd1", ["/custom", "p1", "p2"]),
        # 5) cwd, custom, cwd, PYTHONPATH="cwd1:" -> only first cwd removed; env equals f"{cwd}:"
        (["/cwd1", "/custom", "/cwd1", "p1"], "/cwd1:", ["/custom", "/cwd1", "p1"]),
        # 6) Two cwd entries, PYTHONPATH="cwd1:" -> only first cwd removed
        (["/cwd1", "/cwd1", "p1"], "/cwd1:", ["/cwd1", "p1"]),
        # 7) '', cwd, custom ; PYTHONPATH=":cwd1" -> only '' removed
        (["", "/cwd1", "/custom", "p1"], ":/cwd1", ["/cwd1", "/custom", "p1"]),
        # 8) cwd, custom, cwd ; PYTHONPATH=":cwd1" -> only first cwd removed
        (["/cwd1", "/custom", "/cwd1", "p1"], ":/cwd1", ["/custom", "/cwd1", "p1"]),
        # 9) '', cwd, cwd ; PYTHONPATH=":cwd1" -> only '' removed
        (["", "/cwd1", "/cwd1", "p1"], ":/cwd1", ["/cwd1", "/cwd1", "p1"]),
        # 10) cwd, custom, another ; PYTHONPATH="cwd1:" -> only first cwd removed
        (["/cwd1", "/custom", "/another", "p1"], "/cwd1:", ["/custom", "/another", "p1"]),
    ],
)
def test_modify_sys_path_with_varying_getcwd(initial_paths, pythonpath, expected):
    """
    Ensure modify_sys_path() uses a consistent cwd value across its checks.

    The candidate (faulty) implementation calls os.getcwd() twice and thus if
    os.getcwd() returns different values on consecutive calls (simulated here
    via side_effect) it will behave incorrectly. The gold implementation reads
    cwd once and is stable.
    """
    # Simulate os.getcwd() returning two different values on consecutive calls.
    # The first call should represent the "true" cwd used in comparisons by the
    # gold implementation, while the second call simulates a differing value
    # that would confuse the faulty implementation.
    cwd_first = "/cwd1"
    cwd_second = "/cwd2"
    default_tail = [p for p in initial_paths[2:]] if len(initial_paths) > 2 else []

    with _test_sys_path():
        # Patch os.getcwd to return cwd_first on the first call and cwd_second on the second
        with patch("os.getcwd", side_effect=[cwd_first, cwd_second]) as mock_getcwd:
            # Use a fresh copy of the paths
            sys.path = copy(initial_paths)
            # Ensure PYTHONPATH environment is set per test case
            with _test_environ_pythonpath(pythonpath):
                modify_sys_path()
            # Build expected absolute result: replace symbolic cwd placeholder with cwd_first
            # when needed: our initial_paths use '/cwd1' literal so expected is already correct.
            assert sys.path == expected, (
                f"For initial_paths={initial_paths!r}, PYTHONPATH={pythonpath!r}, "
                f"got sys.path={sys.path!r} but expected {expected!r}"
            )

from copy import copy
from unittest.mock import patch
import pytest
import sys
from pylint import modify_sys_path
from pylint.testutils.utils import _test_sys_path, _test_environ_pythonpath
import sys
from copy import copy
from unittest.mock import patch

import pytest

from pylint import modify_sys_path
from pylint.testutils.utils import _test_sys_path, _test_environ_pythonpath

DEFAULT_PATHS = [
    "/usr/local/lib/python39.zip",
    "/usr/local/lib/python3.9",
    "/usr/local/lib/python3.9/lib-dynload",
    "/usr/local/lib/python3.9/site-packages",
]

@pytest.mark.parametrize(
    "first_entry, env_value, side_effects, expect_contains",
    [
        # 1) leading colon equals first cwd: gold keeps '/custom_pythonpath'
        ("/cwd1", ":/cwd1", ("/cwd1", "/cwd2"), True),
        # 2) trailing colon equals first cwd: gold keeps first default
        ("/cwd1", "/cwd1:", ("/cwd1", "/cwd2"), True),
        # 3) starting with empty first entry and leading colon equals cwd1
        ("", ":/cwd1", ("/cwd1", "/cwd2"), True),
        # 4) starting with '.' first entry and trailing colon equals cwd1
        (".", "/cwd1:", ("/cwd1", "/cwd2"), True),
        # 5) first entry not cwd and leading colon equals cwd1 -> gold leaves sys.path unchanged
        ("/do_not_remove", ":/cwd1", ("/cwd1", "/cwd2"), True),
        # 6) first entry not cwd and trailing colon equals cwd1 -> gold leaves sys.path unchanged
        ("/do_not_remove", "/cwd1:", ("/cwd1", "/cwd2"), True),
        # 7) duplicate cwd entries and leading colon equals cwd1
        ("/cwd1", ":/cwd1", ("/cwd1", "/cwd2"), True),
        # 8) duplicate cwd entries and trailing colon equals cwd1
        ("/cwd1", "/cwd1:", ("/cwd1", "/cwd2"), True),
        # 9) leading colon equals second cwd (cwd2): gold will remove '/custom_pythonpath', candidate keeps it
        ("/cwd1", ":/cwd2", ("/cwd1", "/cwd2"), False),
        # 10) trailing colon equals second cwd (cwd2): gold will remove first default, candidate keeps it
        ("/cwd1", "/cwd2:", ("/cwd1", "/cwd2"), False),
    ],
)
def test_modify_sys_path_cwd_change_variants(
    first_entry, env_value, side_effects, expect_contains
):
    """
    Test various combinations where os.getcwd() returns different values
    on successive calls. The gold patch reads cwd once; the candidate reads it
    twice and therefore can behave differently.
    """
    cwd_first, cwd_second = side_effects
    custom = "/custom_pythonpath"
    # Build initial sys.path for each case. Some cases insert duplicates to match scenarios.
    if first_entry in ("", "."):
        paths = [first_entry, cwd_first, custom, *DEFAULT_PATHS]
    elif first_entry == "/cwd1" and env_value in (":/cwd1", "/cwd1:"):
        # variants that use cwd1 as first entry with a duplicate
        # to emulate scenarios covered by original tests
        paths = [cwd_first, cwd_first, custom, *DEFAULT_PATHS]
    else:
        paths = [first_entry, custom, *DEFAULT_PATHS]

    with _test_sys_path():
        sys.path = copy(paths)
        # Patch os.getcwd to return two different values in sequence
        with patch("os.getcwd", side_effect=[cwd_first, cwd_second]):
            with _test_environ_pythonpath(env_value):
                modify_sys_path()
            if expect_contains:
                # For "expect_contains" True we assert that "/custom_pythonpath" is present
                # or that the original first element is preserved (for non-cwd first entries).
                if first_entry in ("/do_not_remove",):
                    assert sys.path[0] == "/do_not_remove"
                else:
                    assert custom in sys.path, (
                        f"Expected {custom} to remain in sys.path for paths={paths}, "
                        f"PYTHONPATH={env_value}, cwd_first={cwd_first}, cwd_second={cwd_second}. "
                        f"Got sys.path={sys.path}"
                    )
            else:
                # For these cases gold behavior removes the custom path / first default.
                # We assert that '/custom_pythonpath' is NOT present.
                assert custom not in sys.path, (
                    f"Expected {custom} to be removed from sys.path for paths={paths}, "
                    f"PYTHONPATH={env_value}, cwd_first={cwd_first}, cwd_second={cwd_second}. "
                    f"Got sys.path={sys.path}"
                )