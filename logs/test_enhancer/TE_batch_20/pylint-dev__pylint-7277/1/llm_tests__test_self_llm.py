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