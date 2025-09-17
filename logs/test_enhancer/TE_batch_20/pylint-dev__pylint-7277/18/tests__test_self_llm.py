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

from copy import copy
from unittest.mock import patch

# tests/test_modify_sys_path_extra.py
import os
import sys
from copy import copy
from unittest.mock import patch

import pytest

from pylint import modify_sys_path
from pylint.testutils.utils import _test_sys_path, _test_environ_pythonpath

@pytest.mark.parametrize("first,expected", [
    ("/do_not_remove", "/do_not_remove"),
])
def test_no_remove_when_first_path_not_special_and_no_pythonpath(first, expected):
    default_paths = ["/usr/lib/python3.9", "/usr/lib/python3.9/site-packages"]
    with _test_sys_path():
        sys.path = [first, *default_paths]
        with _test_environ_pythonpath():
            modify_sys_path()
        assert sys.path == [first, *default_paths]

def test_remove_empty_string_first_entry():
    cwd = "/tmp/projectcwd"
    default_paths = ["/lib", "/site"]
    with _test_sys_path(), patch("os.getcwd") as mock_getcwd:
        mock_getcwd.return_value = cwd
        sys.path = ["", *default_paths]
        with _test_environ_pythonpath():
            modify_sys_path()
        assert sys.path == default_paths

def test_remove_dot_first_entry():
    cwd = "/some/cwd"
    default_paths = ["/lib", "/site"]
    with _test_sys_path(), patch("os.getcwd") as mock_getcwd:
        mock_getcwd.return_value = cwd
        sys.path = [".", *default_paths]
        with _test_environ_pythonpath():
            modify_sys_path()
        assert sys.path == default_paths

def test_remove_cwd_first_entry_and_preserve_rest():
    cwd = "/home/me/project"
    default_paths = ["/lib", "/site"]
    with _test_sys_path(), patch("os.getcwd") as mock_getcwd:
        mock_getcwd.return_value = cwd
        sys.path = [cwd, *default_paths]
        with _test_environ_pythonpath():
            modify_sys_path()
        assert sys.path == default_paths

def test_pythonpath_starts_colon_removes_additional_leading_entry():
    # Scenario similar to existing coverage but explicit:
    # sys.path begins with cwd, then custom pythonpath entry; PYTHONPATH starts with ":"
    cwd = "/workspace"
    paths = [cwd, "/custom_pythonpath", "/lib"]
    with _test_sys_path(), patch("os.getcwd") as mock_getcwd:
        mock_getcwd.return_value = cwd
        sys.path = copy(paths)
        # PYTHONPATH begins with ":" and is not exactly f":{cwd}" or ":."
        with _test_environ_pythonpath(":/custom_pythonpath"):
            modify_sys_path()
        # first pop removes cwd -> ['/custom_pythonpath','/lib']
        # env.startswith(':') triggers another pop(0) -> ['/lib']
        assert sys.path == ["/lib"]

def test_pythonpath_ends_colon_removes_middle_entry():
    cwd = "/project"
    paths = [cwd, "/custom_pythonpath", cwd, "/lib"]
    with _test_sys_path(), patch("os.getcwd") as mock_getcwd:
        mock_getcwd.return_value = cwd
        sys.path = copy(paths)
        # PYTHONPATH ends with ":" and is not exactly f"{cwd}:" or ".:"
        with _test_environ_pythonpath("/custom_pythonpath:"):
            modify_sys_path()
        # After first pop(0) -> ['/custom_pythonpath', cwd, '/lib']
        # env.endswith(':') branch pops index 1 -> ['/custom_pythonpath', '/lib']
        assert sys.path == ["/custom_pythonpath", "/lib"]

def test_no_second_pop_when_pythonpath_equals_colon_cwd():
    cwd = "/home/alice"
    paths = [cwd, "/custom_pythonpath"]
    with _test_sys_path(), patch("os.getcwd") as mock_getcwd:
        mock_getcwd.return_value = cwd
        sys.path = copy(paths)
        # PYTHONPATH is exactly f":{cwd}" so second pop should be skipped
        with _test_environ_pythonpath(f":{cwd}"):
            modify_sys_path()
        # only initial cwd is removed
        assert sys.path == ["/custom_pythonpath"]

def test_no_second_pop_when_pythonpath_equals_cwd_colon():
    cwd = "/var/www"
    paths = [cwd, "/custom_pythonpath"]
    with _test_sys_path(), patch("os.getcwd") as mock_getcwd:
        mock_getcwd.return_value = cwd
        sys.path = copy(paths)
        # PYTHONPATH is exactly f"{cwd}:" so second pop should be skipped
        with _test_environ_pythonpath(f"{cwd}:"):
            modify_sys_path()
        assert sys.path == ["/custom_pythonpath"]

def test_skip_pythonpath_rules_when_pythonpath_is_dot_colon():
    cwd = "/tmp/dir"
    paths = ["", cwd, cwd, "/lib"]
    with _test_sys_path(), patch("os.getcwd") as mock_getcwd:
        mock_getcwd.return_value = cwd
        sys.path = copy(paths)
        # PYTHONPATH is ":." which should prevent env-based popping
        with _test_environ_pythonpath(":."):
            modify_sys_path()
        # initial empty element removed, env-based removal skipped
        assert sys.path == [cwd, cwd, "/lib"]

def test_single_element_sys_path_equals_cwd_and_pythonpath_matches_colon_cwd_no_error():
    cwd = "/onlycwd"
    with _test_sys_path(), patch("os.getcwd") as mock_getcwd:
        mock_getcwd.return_value = cwd
        sys.path = [cwd]
        # PYTHONPATH equal to f":{cwd}" avoids extra pops and should not raise
        with _test_environ_pythonpath(f":{cwd}"):
            modify_sys_path()
        assert sys.path == []

# No new imports required beyond those inside the test file.
import os
import sys
from copy import deepcopy

import pytest

from pylint import modify_sys_path

def _run_with_env_and_path(cwd, initial_sys_path, pythonpath_value):
    """Helper to run modify_sys_path with controlled cwd, sys.path and PYTHONPATH.
    Returns the resulting sys.path (a copy). Restores original sys.path and PYTHONPATH.
    """
    # Save originals
    orig_sys_path = deepcopy(sys.path)
    orig_environ = os.environ.get("PYTHONPATH", None)
    # Set up
    sys.path = list(initial_sys_path)
    os.environ.pop("PYTHONPATH", None)
    if pythonpath_value is not None:
        os.environ["PYTHONPATH"] = pythonpath_value
    # Patch cwd via monkeypatch-like approach by temporarily replacing os.getcwd
    orig_getcwd = os.getcwd
    try:
        os.getcwd = lambda: cwd  # type: ignore[assignment]
        modify_sys_path()
        result = deepcopy(sys.path)
    finally:
        # Restore
        sys.path = orig_sys_path
        if orig_environ is None:
            os.environ.pop("PYTHONPATH", None)
        else:
            os.environ["PYTHONPATH"] = orig_environ
        os.getcwd = orig_getcwd
    return result

def test_remove_first_entry_when_cwd_at_start():
    cwd = "/fake/cwd"
    default_paths = ["/usr/lib/python3.9", "/usr/lib/python3.9/site-packages"]
    initial = [cwd, *default_paths]
    result = _run_with_env_and_path(cwd, initial, None)
    assert result == initial[1:]

def test_remove_first_entry_when_empty_string_at_start():
    cwd = "/fake/cwd"
    default_paths = ["/usr/lib/python3.9", "/usr/lib/python3.9/site-packages"]
    initial = ["", *default_paths]
    result = _run_with_env_and_path(cwd, initial, None)
    assert result == initial[1:]

def test_remove_first_entry_when_dot_at_start():
    cwd = "/fake/cwd"
    default_paths = ["/usr/lib/python3.9", "/usr/lib/python3.9/site-packages"]
    initial = [".", *default_paths]
    result = _run_with_env_and_path(cwd, initial, None)
    assert result == initial[1:]

def test_do_not_modify_when_first_not_cwd_or_markers():
    cwd = "/fake/cwd"
    default_paths = ["/usr/lib/python3.9", "/usr/lib/python3.9/site-packages"]
    initial = ["/should_not_remove", *default_paths]
    result = _run_with_env_and_path(cwd, initial, None)
    assert result == initial

def test_strip_second_entry_when_pythonpath_starts_with_colon():
    # PYTHONPATH like ":/custom" should cause removal of the (new) first entry
    cwd = "/fake/cwd"
    initial = [cwd, "/custom_pythonpath", "/other"]
    # After first pop -> ["/custom_pythonpath", "/other"]
    # Since PYTHONPATH startswith ":" and is not exactly f":{cwd}" nor ":.",
    # modify_sys_path should pop the current first entry again (pop(0)),
    # resulting in ["/other"]
    result = _run_with_env_and_path(cwd, initial, ":/custom_pythonpath")
    assert result == ["/other"]

def test_do_not_strip_when_pythonpath_is_colon_prefixed_cwd_marker():
    # PYTHONPATH == f":{cwd}" should NOT trigger an extra pop
    cwd = "/fake/cwd"
    initial = [cwd, cwd, "/other"]
    # After first pop -> [cwd, "/other"]
    # PYTHONPATH == f":{cwd}" -> should not trigger the extra pop
    result = _run_with_env_and_path(cwd, initial, f":{cwd}")
    assert result == [cwd, "/other"]

def test_remove_second_entry_when_pythonpath_ends_with_colon():
    # PYTHONPATH like "/custom:" should cause pop(1) when appropriate
    cwd = "/fake/cwd"
    initial = [cwd, "/custom_pythonpath", cwd, "/more"]
    # After first pop -> ["/custom_pythonpath", cwd, "/more"]
    # PYTHONPATH endswith ":" and is not f"{cwd}:" nor ".:" -> pop(1) removes cwd
    result = _run_with_env_and_path(cwd, initial, "/custom_pythonpath:")
    assert result == ["/custom_pythonpath", "/more"]

def test_do_not_pop_second_when_pythonpath_ends_with_cwd_colon_marker():
    cwd = "/fake/cwd"
    initial = [cwd, "/custom_pythonpath", "/more"]
    # After first pop -> ["/custom_pythonpath", "/more"]
    # PYTHONPATH == f"{cwd}:" should NOT trigger pop(1) -> no further removal
    result = _run_with_env_and_path(cwd, initial, f"{cwd}:")
    assert result == ["/custom_pythonpath", "/more"]

def test_multiple_cwd_entries_at_end_not_removed():
    # Ensure trailing cwd entries (e.g., editable install) are not removed
    cwd = "/fake/cwd"
    default_paths = ["/usr/lib/python3.9", "/usr/lib/python3.9/site-packages"]
    initial = [cwd, *default_paths, cwd]
    result = _run_with_env_and_path(cwd, initial, None)
    # Only the first occurrence should be removed, trailing one should stay
    assert result == [*default_paths, cwd]

def test_no_exception_when_pythonpath_not_set():
    # If PYTHONPATH is absent, modify_sys_path should run without raising
    cwd = "/fake/cwd"
    initial = [cwd, "/a", "/b"]
    result = _run_with_env_and_path(cwd, initial, None)
    assert result == ["/a", "/b"]

# No extra imports required beyond those included in the test file.
# tests/test_modify_sys_path_consistency.py
import os
import sys
from copy import copy
from unittest.mock import patch

import pytest

from pylint import modify_sys_path

DEFAULT_PATHS = [
    "/usr/local/lib/python39.zip",
    "/usr/local/lib/python3.9",
    "/usr/local/lib/python3.9/lib-dynload",
    "/usr/local/lib/python3.9/site-packages",
]

CWD1 = "/tmp/cwd_one"
CWD2 = "/tmp/cwd_two"

def _compute_expected_with_consistent_cwd(initial_paths, pythonpath, cwd_value):
    """
    Helper: compute expected sys.path after modify_sys_path by forcing
    os.getcwd() to consistently return cwd_value for all calls.
    """
    orig_path = copy(sys.path)
    try:
        sys.path = copy(initial_paths)
        if pythonpath is None:
            os.environ.pop("PYTHONPATH", None)
        else:
            os.environ["PYTHONPATH"] = pythonpath
        with patch("os.getcwd", return_value=cwd_value):
            modify_sys_path()
        return copy(sys.path)
    finally:
        sys.path = orig_path
        os.environ.pop("PYTHONPATH", None)

def _run_with_inconsistent_getcwd(initial_paths, pythonpath, first_cwd, second_cwd):
    """
    Run modify_sys_path with os.getcwd() returning first_cwd then second_cwd.
    """
    orig_path = copy(sys.path)
    try:
        sys.path = copy(initial_paths)
        if pythonpath is None:
            os.environ.pop("PYTHONPATH", None)
        else:
            os.environ["PYTHONPATH"] = pythonpath
        with patch("os.getcwd", side_effect=[first_cwd, second_cwd]):
            modify_sys_path()
        return copy(sys.path)
    finally:
        sys.path = orig_path
        os.environ.pop("PYTHONPATH", None)

@pytest.mark.parametrize(
    "initial,pythonpath",
    [
        # 1: duplicated cwd entries, PYTHONPATH starts with :{cwd}
        ([CWD1, CWD1] + DEFAULT_PATHS, f":{CWD1}"),
        # 2: single cwd then custom entry, PYTHONPATH equals {cwd}:
        ([CWD1, "/custom"] + DEFAULT_PATHS, f"{CWD1}:"),
        # 3: empty first entry, followed by duplicated cwd entries, PYTHONPATH starts with :{cwd}
        (["", CWD1, CWD1] + DEFAULT_PATHS, f":{CWD1}"),
        # 4: dot as first entry, then cwd and custom, PYTHONPATH equals {cwd}:
        ([".", CWD1, "/custom"] + DEFAULT_PATHS, f"{CWD1}:"),
        # 5: first is cwd, second is different cwd, PYTHONPATH starts with :{first_cwd}
        ([CWD1, CWD2] + DEFAULT_PATHS, f":{CWD1}"),
        # 6: duplicated cwd entries with trailing custom, PYTHONPATH equals {cwd}:
        ([CWD1, CWD1, "/custom"] + DEFAULT_PATHS, f"{CWD1}:"),
        # 7: cwd, custom, cwd; PYTHONPATH starts with :{cwd}
        ([CWD1, "/custom", CWD1] + DEFAULT_PATHS, f":{CWD1}"),
        # 8: empty, cwd, custom; PYTHONPATH equals {cwd}:
        (["", CWD1, "/custom"] + DEFAULT_PATHS, f"{CWD1}:"),
        # 9: multiple cwd occurrences including trailing entry; PYTHONPATH startswith :{cwd}
        ([CWD1, CWD1] + DEFAULT_PATHS + [CWD1], f":{CWD1}"),
        #10: cwd followed by two non-cwd entries; PYTHONPATH equals {cwd}:
        ([CWD1, "/custom", "/other"] + DEFAULT_PATHS, f"{CWD1}:"),
    ],
)
def test_modify_sys_path_consistent_vs_inconsistent_getcwd(initial, pythonpath):
    """
    For each scenario compute expected result when os.getcwd is consistent
    (always returns CWD1) and compare to result when os.getcwd returns
    CWD1 first and CWD2 second. Under the correct implementation both
    results must match.
    """
    expected = _compute_expected_with_consistent_cwd(initial, pythonpath, CWD1)
    result = _run_with_inconsistent_getcwd(initial, pythonpath, CWD1, CWD2)
    assert result == expected, (
        "modify_sys_path must behave the same when os.getcwd() is called "
        "multiple times; inconsistent getcwd led to divergent sys.path. "
        f"initial={initial!r}, PYTHONPATH={pythonpath!r}, expected={expected!r}, got={result!r}"
    )

from copy import copy
from unittest.mock import patch
import os
import sys
import pytest
# tests/test_modify_sys_path_extra.py
import os
from copy import copy
from unittest.mock import patch

import pytest

from pylint import modify_sys_path
from pylint.testutils.utils import _test_environ_pythonpath, _test_sys_path


@pytest.mark.parametrize(
    "first,expected_first_removed",
    [
        ("/some/other", False),
        ("", True),
        (".", True),
    ],
)
def test_remove_first_only_for_empty_dot_or_cwd(first, expected_first_removed, tmp_path):
    # Ensure behavior for first element being "", "." or other path
    default_paths = [str(tmp_path / "lib1"), str(tmp_path / "lib2")]
    cwd = "/current/working/dir"
    with _test_sys_path(), patch("os.getcwd") as mock_getcwd:
        mock_getcwd.return_value = cwd
        paths = [first, *default_paths]
        # If first equals cwd we want to exercise that case as well
        if first == "/cwd_marker_for_test":
            paths[0] = cwd
        # set sys.path
        import sys
        sys.path = copy(paths)
        with _test_environ_pythonpath():
            modify_sys_path()
        if expected_first_removed:
            assert sys.path == default_paths
        else:
            assert sys.path == paths


def test_remove_first_when_first_is_cwd():
    # When first element equals current working directory it must be removed
    default_paths = ["/usr/lib/python", "/usr/lib/python/lib-dynload"]
    cwd = "/i/am/cwd"
    with _test_sys_path(), patch("os.getcwd") as mock_getcwd:
        mock_getcwd.return_value = cwd
        paths = [cwd, *default_paths]
        import sys
        sys.path = copy(paths)
        with _test_environ_pythonpath():
            modify_sys_path()
        assert sys.path == default_paths


def test_pythonpath_startswith_colon_removes_second_entry_when_not_excluded():
    # If PYTHONPATH starts with ":" and is not exactly :{cwd} or :. remove the
    # current first element (after initial stripping)
    default_paths = ["/p1", "/p2", "/p3"]
    cwd = "/mycwd"
    with _test_sys_path(), patch("os.getcwd") as mock_getcwd:
        mock_getcwd.return_value = cwd
        # include cwd as first to trigger its removal first
        paths = [cwd, "/other", *default_paths]
        import sys
        sys.path = copy(paths)
        with _test_environ_pythonpath(":/other:more"):
            modify_sys_path()
        # first removal removes cwd, then env-pythonpath startswith ":" and is not f":{cwd}"
        # so another pop(0) removes "/other", leaving default_paths
        assert sys.path == default_paths


def test_pythonpath_startswith_colon_but_excluded_by_exact_match():
    # If PYTHONPATH is exactly :{cwd} or :. we must NOT remove the second item
    default_paths = ["/p1", "/p2"]
    cwd = "/home/cwd"
    with _test_sys_path(), patch("os.getcwd") as mock_getcwd:
        mock_getcwd.return_value = cwd
        paths = [cwd, "/second", *default_paths]
        import sys
        sys.path = copy(paths)
        # exact match :{cwd} should prevent the additional pop
        with _test_environ_pythonpath(f":{cwd}"):
            modify_sys_path()
        assert sys.path == ["/second", *default_paths]

        # exact match :. should also prevent additional pop
        sys.path = copy(paths)
        with _test_environ_pythonpath(":.") :
            modify_sys_path()
        assert sys.path == ["/second", *default_paths]


def test_pythonpath_endswith_colon_removes_third_entry_when_not_excluded():
    # If PYTHONPATH ends with ":" and is not exactly {cwd}: or .:, remove the
    # second element (index 1) (after possibly removing the first)
    default_paths = ["/pA", "/pB", "/pC"]
    cwd = "/c"
    with _test_sys_path(), patch("os.getcwd") as mock_getcwd:
        mock_getcwd.return_value = cwd
        paths = [cwd, "/custom_pythonpath", "/another", *default_paths]
        import sys
        sys.path = copy(paths)
        with _test_environ_pythonpath("/custom_pythonpath:"):
            modify_sys_path()
        # initial pop removes cwd, env endswith ":" triggers pop(1) which removes "/another"
        # resulting sys.path should be ["/custom_pythonpath", *default_paths]
        assert sys.path == ["/custom_pythonpath", *default_paths]


def test_pythonpath_endswith_colon_but_excluded_by_exact_match():
    default_paths = ["/pX", "/pY"]
    cwd = "/mycwd2"
    with _test_sys_path(), patch("os.getcwd") as mock_getcwd:
        mock_getcwd.return_value = cwd
        paths = [cwd, "/second", *default_paths]
        import sys
        sys.path = copy(paths)
        # exact match {cwd}: should prevent removal via endswith branch
        with _test_environ_pythonpath(f"{cwd}:"):
            modify_sys_path()
        assert sys.path == ["/second", *default_paths]

        sys.path = copy(paths)
        with _test_environ_pythonpath(".:"):
            modify_sys_path()
        assert sys.path == ["/second", *default_paths]


def test_multiple_cwd_entries_and_colon_variants():
    # Complex case: multiple cwd entries together with PYTHONPATH variants
    default_paths = ["/lib1", "/lib2", "/lib3"]
    cwd = "/repeat_cwd"
    with _test_sys_path(), patch("os.getcwd") as mock_getcwd:
        mock_getcwd.return_value = cwd
        paths = [cwd, cwd, "/custom", *default_paths]
        import sys
        sys.path = copy(paths)
        # when PYTHONPATH is ":" at the end it should remove one cwd from front and then
        # the second branch should remove the third entry in original list
        with _test_environ_pythonpath(":/custom:"):
            modify_sys_path()
        # After first pop -> [cwd, "/custom", ...]
        # env startswith ":" True -> pop(0) removes cwd -> ["/custom", ...]
        assert sys.path == ["/custom", *default_paths]

def test_no_change_when_first_is_not_dot_empty_or_cwd_and_no_pythonpath_colons():
    default_paths = ["/A", "/B", "/C"]
    cwd = "/somecwd"
    with _test_sys_path(), patch("os.getcwd") as mock_getcwd:
        mock_getcwd.return_value = cwd
        paths = ["/do_not_remove", *default_paths]
        import sys
        sys.path = copy(paths)
        with _test_environ_pythonpath(""):
            modify_sys_path()
        assert sys.path == paths

# No new imports required beyond those inside the test module itself.
import os
import sys
from copy import copy
from unittest.mock import patch

import pytest

from pylint import modify_sys_path

def _run_modify_sys_path_with(cwd, paths, pythonpath):
    """Helper to run modify_sys_path with controlled cwd, sys.path, and PYTHONPATH.

    Returns a new list with the resulting sys.path after calling modify_sys_path.
    """
    original_sys_path = copy(sys.path)
    try:
        sys.path = copy(paths)
        if pythonpath is None:
            # ensure it's not set
            if "PYTHONPATH" in os.environ:
                del os.environ["PYTHONPATH"]
        else:
            os.environ["PYTHONPATH"] = pythonpath
        with patch("os.getcwd", return_value=cwd):
            modify_sys_path()
        return copy(sys.path)
    finally:
        sys.path = original_sys_path
        # restore env
        if "PYTHONPATH" in os.environ:
            del os.environ["PYTHONPATH"]

def test_remove_cwd_at_start_without_pythonpath():
    cwd = "/home/user/project"
    default_paths = ["/usr/lib/python3.9", "/usr/lib/python3.9/site-packages"]
    paths = [cwd, *default_paths]
    result = _run_modify_sys_path_with(cwd, paths, None)
    assert result == default_paths

def test_remove_empty_string_at_start_without_pythonpath():
    cwd = "/home/user/project"
    default_paths = ["/usr/lib/python3.9", "/usr/lib/python3.9/site-packages"]
    paths = ["", *default_paths]
    result = _run_modify_sys_path_with(cwd, paths, None)
    assert result == default_paths

def test_remove_dot_at_start_without_pythonpath():
    cwd = "/home/user/project"
    default_paths = ["/usr/lib/python3.9", "/usr/lib/python3.9/site-packages"]
    paths = [".", *default_paths]
    result = _run_modify_sys_path_with(cwd, paths, None)
    assert result == default_paths

def test_do_not_remove_when_first_is_otherpath():
    cwd = "/home/user/project"
    default_paths = ["/usr/lib/python3.9", "/usr/lib/python3.9/site-packages"]
    paths = ["/do_not_remove", *default_paths]
    result = _run_modify_sys_path_with(cwd, paths, None)
    assert result == paths

def test_leading_colon_pythonpath_removes_second_entry_when_not_cwd():
    cwd = "/home/user/project"
    default_paths = ["/usr/lib/python3.9", "/usr/lib/python3.9/site-packages"]
    # sys.path starts with cwd then a custom path (should remove first then because PYTHONPATH starts with ":" remove next)
    paths = [cwd, "/custom_pythonpath", *default_paths]
    result = _run_modify_sys_path_with(cwd, paths, ":/custom_pythonpath")
    # Expected: first cwd removed by initial rule, then because PYTHONPATH startswith ":" and not equal to f":{cwd}"
    # pop(0) again, leaving the remainder starting from what was originally index 2
    assert result == default_paths

def test_trailing_colon_pythonpath_removes_second_entry_index_1_not_0():
    cwd = "/home/user/project"
    default_paths = ["/usr/lib/python3.9", "/usr/lib/python3.9/site-packages"]
    paths = [cwd, "/custom_pythonpath", *default_paths]
    # With PYTHONPATH ending with ":" and not equal to f"{cwd}:" we should pop index 1 (the "/custom_pythonpath")
    result = _run_modify_sys_path_with(cwd, paths, "/custom_pythonpath:")
    # After initial removal of cwd, popping index 1 corresponds to removing the original index 2.
    # BUT the intended behavior is to remove the second entry (index 1) iff trailing ":" and not pointing to cwd,
    # so the remaining path should start with what was originally paths[1] if cwd was not removed,
    # however since the first element is cwd it gets removed first, and then index 1 (new) is popped.
    # The expected remainder is [paths[1]] + paths[3:], which simplifies to ['/custom_pythonpath'] removed -> default_paths
    assert result == default_paths

def test_do_not_remove_on_pythonpath_pointing_to_cwd_with_leading_colon():
    cwd = "/home/user/project"
    default_paths = ["/usr/lib/python3.9", "/usr/lib/python3.9/site-packages"]
    paths = [cwd, cwd, *default_paths]
    # PYTHONPATH equal to f":{cwd}" should not trigger the additional removal
    result = _run_modify_sys_path_with(cwd, paths, f":{cwd}")
    # only the first cwd should be removed (the normal removal)
    assert result == [cwd, *default_paths]

def test_do_not_remove_on_pythonpath_pointing_to_cwd_with_trailing_colon():
    cwd = "/home/user/project"
    default_paths = ["/usr/lib/python3.9", "/usr/lib/python3.9/site-packages"]
    paths = [cwd, cwd, *default_paths]
    # PYTHONPATH equal to f"{cwd}:" should not trigger the additional removal
    result = _run_modify_sys_path_with(cwd, paths, f"{cwd}:")
    # only the first cwd should be removed (the normal removal)
    assert result == [cwd, *default_paths]

def test_leading_colon_with_explicit_dot_should_not_remove_second_if_dot_refers_to_cwd():
    # If PYTHONPATH is ":." and the cwd is present we must NOT remove the second entry
    cwd = "/home/user/project"
    default_paths = ["/usr/lib/python3.9", "/usr/lib/python3.9/site-packages"]
    paths = [cwd, "/custom_pythonpath", *default_paths]
    result = _run_modify_sys_path_with(cwd, paths, ":.")
    # Only the first entry should have been removed (the cwd)
    assert result == ["/custom_pythonpath", *default_paths]

# no new imports required beyond standard pytest fixtures and builtins
# tests/test_modify_sys_path_regression.py
import os
import sys
from copy import copy

import pytest

from pylint import modify_sys_path


def _sequential_getcwd(monkeypatch, values):
    """Patch os.getcwd to return values sequentially on each call,
    and then keep returning the last value."""
    it = iter(values)

    def _getcwd():
        try:
            return next(it)
        except StopIteration:
            return values[-1]

    monkeypatch.setattr(os, "getcwd", _getcwd)


@pytest.mark.parametrize(
    "initial_sys_path, pythonpath, expected",
    [
        # 1: first element equals original cwd, PYTHONPATH startswith ":" and equals ":orig"
        (["/orig_cwd", "/custom", "/other"], ":/orig_cwd", ["/custom", "/other"]),
        # 2: first element is empty string, PYTHONPATH startswith ":" and equals ":orig"
        (["", "/custom", "/other"], ":/orig_cwd", ["/custom", "/other"]),
        # 3: first element equals orig and there is another orig later;
        # PYTHONPATH endswith ":" and equals "orig:" -> should not remove second entry
        (["/orig_cwd", "/custom", "/orig_cwd", "/other"], "/orig_cwd:", ["/custom", "/orig_cwd", "/other"]),
        # 4: first element does not equal cwd and PYTHONPATH startswith ":orig" -> no change expected
        (["/do_not_remove", "/custom", "/other"], ":/orig_cwd", ["/do_not_remove", "/custom", "/other"]),
        # 5: first element does not equal cwd and PYTHONPATH endswith "orig:" -> no change expected
        (["/do_not_remove", "/custom", "/other"], "/orig_cwd:", ["/do_not_remove", "/custom", "/other"]),
        # 6: two leading cwd entries and PYTHONPATH startswith ":orig" -> only one leading cwd removed
        (["/orig_cwd", "/orig_cwd", "/custom", "/other"], ":/orig_cwd", ["/orig_cwd", "/custom", "/other"]),
        # 7: first element is ".", PYTHONPATH startswith ":orig" -> should remove the "." only once
        ([".", "/custom", "/other"], ":/orig_cwd", ["/custom", "/other"]),
        # 8: first element is ".", PYTHONPATH endswith "orig:" -> should not remove second element
        ([".", "/custom", "/other"], "/orig_cwd:", ["/custom", "/other"]),
        # 9: cwd appears trailing and PYTHONPATH startswith ":orig" -> only leading cwd removed
        (["/orig_cwd", "/custom", "/other", "/orig_cwd"], ":/orig_cwd", ["/custom", "/other", "/orig_cwd"]),
        # 10: first element does not equal cwd and PYTHONPATH endswith colon with different cwd -> no change
        (["/somewhere", "/custom", "/other"], "/orig_cwd:", ["/somewhere", "/custom", "/other"]),
    ],
)
def test_modify_sys_path_with_changing_cwd(
    monkeypatch, initial_sys_path, pythonpath, expected
):
    """
    Simulate os.getcwd returning different values on successive calls.
    The gold patch reads cwd once and should produce `expected`. The buggy
    model patch reads cwd twice and may modify sys.path further; these tests
    will fail against that buggy behavior.
    """
    # Save and restore original sys.path
    original_sys_path = copy(sys.path)
    try:
        # Prepare a sequential getcwd: first call returns "/orig_cwd", second returns "/new_cwd"
        _sequential_getcwd(monkeypatch, ["/orig_cwd", "/new_cwd"])

        # Set environment variable
        monkeypatch.setenv("PYTHONPATH", pythonpath)

        # Set sys.path to the test initial value
        sys.path = copy(initial_sys_path)

        # Call the function under test
        modify_sys_path()

        assert sys.path == expected
    finally:
        sys.path = original_sys_path
        # Clean PYTHONPATH to avoid leaking environment changes
        monkeypatch.delenv("PYTHONPATH", raising=False)

# No new imports required beyond those present in the test code block.
import sys
from copy import copy
from unittest.mock import patch

import pytest

from pylint import modify_sys_path
from pylint.testutils.utils import _test_sys_path, _test_environ_pythonpath


# Re-usable default tail used in many scenarios
DEFAULT_TAIL = ["/usr/local/lib/python39.zip", "/usr/local/lib/python3.9"]


def _make_paths(*head):
    return list(head) + DEFAULT_TAIL


def test_cwd_changed_leading_colon_equals_new_cwd():
    """If os.getcwd() changes between calls and PYTHONPATH starts with :{new_cwd},
    the gold implementation should remove two leading entries when the first entry
    equals the original cwd. A broken implementation that samples os.getcwd()
    twice may skip the second removal."""
    cwd1 = "/original/cwd"
    cwd2 = "/changed/cwd"
    paths = _make_paths(cwd1, cwd1, "/p1", "/p2")
    with _test_sys_path():
        with patch("os.getcwd") as mock_getcwd:
            mock_getcwd.side_effect = [cwd1, cwd2]
            sys.path = copy(paths)
            with _test_environ_pythonpath(f":{cwd2}"):
                modify_sys_path()
            # Gold behavior: first pop removes the original cwd, second pop removes
            # the subsequent cwd entry because PYTHONPATH != f":{cwd1}"
            assert sys.path == paths[2:]


def test_empty_first_element_and_leading_colon_matching_new_cwd():
    """First element is '', and PYTHONPATH equals :{new_cwd}.
    The correct behavior removes two leading entries; an incorrect implementation
    sampling getcwd twice may only remove one."""
    cwd1 = "/orig"
    cwd2 = "/new"
    paths = _make_paths("", cwd1, "/custom")
    with _test_sys_path():
        with patch("os.getcwd") as mock_getcwd:
            mock_getcwd.side_effect = [cwd1, cwd2]
            sys.path = copy(paths)
            with _test_environ_pythonpath(f":{cwd2}"):
                modify_sys_path()
            assert sys.path == paths[2:]


def test_trailing_colon_and_changed_cwd_removes_index_one():
    """When PYTHONPATH ends with {new_cwd}: and first entry is original cwd,
    the correct implementation removes the original cwd and then removes the
    element at index 1 of the remaining list. A buggy implementation sampling
    os.getcwd twice may skip the second removal."""
    cwd1 = "/origC"
    cwd2 = "/newC"
    # Start with original cwd, then a custom entry, then a copy of cwd1, then defaults
    paths = _make_paths(cwd1, "/custom_pythonpath", cwd1, "/p1")
    with _test_sys_path():
        with patch("os.getcwd") as mock_getcwd:
            mock_getcwd.side_effect = [cwd1, cwd2]
            sys.path = copy(paths)
            with _test_environ_pythonpath(f"{cwd2}:"):
                modify_sys_path()
            # Gold behavior: first pop removes cwd1 -> ["/custom_pythonpath", cwd1, ...]
            # then trailing-colon rule removes index 1 (cwd1) -> final should be starting at index 2
            assert sys.path == paths[2:]


def test_no_initial_pop_but_leading_colon_removes_first_when_not_cwd():
    """When first sys.path element is not '', '.', or cwd, but PYTHONPATH starts
    with a ':', the gold implementation will *still* remove the first element.
    If os.getcwd is sampled twice and changes to match PYTHONPATH, a faulty
    implementation may avoid removing it; this test catches that."""
    cwd1 = "/origX"
    cwd2 = "/newX"
    paths = _make_paths("/do_not_remove", "/rest")
    with _test_sys_path():
        with patch("os.getcwd") as mock_getcwd:
            mock_getcwd.side_effect = [cwd1, cwd2]
            sys.path = copy(paths)
            with _test_environ_pythonpath(f":{cwd2}"):
                modify_sys_path()
            # Gold: first element is not special, but PYTHONPATH startswith ":" and is not equal
            # to f":{cwd1}" so we pop the first element -> final is paths[1:]
            assert sys.path == paths[1:]


def test_no_initial_pop_but_trailing_colon_removes_index_one():
    """When first element not in special set and PYTHONPATH ends with '{new_cwd}:',
    gold implementation removes the first element (pop(0)) and then removes index 1
    (pop(1)) of the remaining list. A bad implementation sampling getcwd twice may not."""
    cwd1 = "/origY"
    cwd2 = "/newY"
    paths = _make_paths("/keepme", "/custom", "/extra")
    with _test_sys_path():
        with patch("os.getcwd") as mock_getcwd:
            mock_getcwd.side_effect = [cwd1, cwd2]
            sys.path = copy(paths)
            with _test_environ_pythonpath(f"/custom:{cwd2}:".rstrip(":")):
                # Using a string that ends with ":" is the important part; ensure we pass it properly
                modify_sys_path()
            # Gold: since first element isn't special, but trailing-colon rule applies,
            # pop(0) then pop(1) on the remaining list -> final is paths[2:]
            assert sys.path == paths[2:]


def test_mixed_dot_and_changed_cwd_leading_colon():
    """When sys.path starts with '.' and os.getcwd changes, ensure two pops occur
    (first for '.', second because of leading colon mismatch with original cwd)."""
    cwd1 = "/start"
    cwd2 = "/later"
    paths = _make_paths(".", cwd1, "/z")
    with _test_sys_path():
        with patch("os.getcwd") as mock_getcwd:
            mock_getcwd.side_effect = [cwd1, cwd2]
            sys.path = copy(paths)
            with _test_environ_pythonpath(f":{cwd2}"):
                modify_sys_path()
            assert sys.path == paths[2:]


def test_multiple_cwd_occurrences_and_leading_colon():
    """Multiple occurrences of the original cwd at the start should be popped twice
    with a leading colon PYTHONPATH that does not match f':{original_cwd}'."""
    cwd1 = "/multi"
    cwd2 = "/other"
    paths = _make_paths(cwd1, cwd1, cwd1, "/tail")
    with _test_sys_path():
        with patch("os.getcwd") as mock_getcwd:
            mock_getcwd.side_effect = [cwd1, cwd2]
            sys.path = copy(paths)
            with _test_environ_pythonpath(f":{cwd2}"):
                modify_sys_path()
            # Gold: pop first (cwd1), then pop again due to leading colon != f":{cwd1}"
            assert sys.path == paths[2:]


def test_first_is_cwd_but_pythonpath_equals_original_cwd_colon():
    """If PYTHONPATH starts with :{original_cwd}, then after removing the first element
    (original cwd), the second removal should be skipped. This ensures the function
    properly compares against the original cwd."""
    cwd1 = "/origZ"
    cwd2 = "/origZ"  # intentionally same to ensure no second pop
    paths = _make_paths(cwd1, cwd1, "/a", "/b")
    with _test_sys_path():
        with patch("os.getcwd") as mock_getcwd:
            # Both calls return the same value: this shouldn't be an edge case,
            # and behavior should be to remove two entries only if PYTHONPATH != f":{cwd1}"
            mock_getcwd.side_effect = [cwd1, cwd2]
            sys.path = copy(paths)
            with _test_environ_pythonpath(f":{cwd1}"):
                modify_sys_path()
            # Since PYTHONPATH == f":{cwd1}" we must not perform the second pop; gold ends up with paths[1:]
            assert sys.path == paths[1:]


def test_first_not_cwd_and_pythonpath_equals_new_cwd_leading_colon():
    """When the first element is not special but PYTHONPATH equals :{new_cwd},
    and os.getcwd changes, gold will pop once (because env != f':{original_cwd}')
    whereas a double-getcwd sampling implementation may not pop at all."""
    cwd1 = "/alpha"
    cwd2 = "/beta"
    paths = _make_paths("/notcwd", "/something", "/z")
    with _test_sys_path():
        with patch("os.getcwd") as mock_getcwd:
            mock_getcwd.side_effect = [cwd1, cwd2]
            sys.path = copy(paths)
            with _test_environ_pythonpath(f":{cwd2}"):
                modify_sys_path()
            # Gold: since first element isn't in special set, but PYTHONPATH doesn't equal f":{cwd1}",
            # remove the first element only.
            assert sys.path == paths[1:]