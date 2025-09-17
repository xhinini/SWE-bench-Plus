import pytest
from ... import units as u
# -*- coding: utf-8 -*-
import pytest
from ... import units as u


class OtherTrue:
    def __eq__(self, other):
        # Always claim equality to detect whether this __eq__ is actually called
        return True


class OtherRaises:
    def __eq__(self, other):
        # Raise a distinct exception to ensure it propagates when expected
        raise RuntimeError("other_eq_called")


def test_unit_eq_delegates_to_other_true_left():
    """u.m == OtherTrue() should delegate to OtherTrue.__eq__ and return True."""
    assert u.m == OtherTrue()


def test_unit_eq_delegates_to_other_true_right():
    """OtherTrue() == u.m should call OtherTrue.__eq__ directly and return True."""
    assert OtherTrue() == u.m


def test_unit_eq_delegates_to_other_raises_left():
    """If OtherRaises.__eq__ raises, that exception should propagate when comparing u.m == OtherRaises()."""
    with pytest.raises(RuntimeError, match="other_eq_called"):
        _ = (u.m == OtherRaises())


def test_unit_eq_delegates_to_other_raises_right():
    """If OtherRaises.__eq__ raises, that exception should propagate when comparing OtherRaises() == u.m."""
    with pytest.raises(RuntimeError, match="other_eq_called"):
        _ = (OtherRaises() == u.m)


def test_unrecognizedunit_eq_delegates_to_other_true_left():
    """UnrecognizedUnit == OtherTrue() should delegate to OtherTrue.__eq__ and return True."""
    unrec = u.Unit("FOO", parse_strict='silent')
    assert unrec == OtherTrue()


def test_unrecognizedunit_eq_delegates_to_other_true_right():
    """OtherTrue() == UnrecognizedUnit should call OtherTrue.__eq__ and return True."""
    unrec = u.Unit("FOO", parse_strict='silent')
    assert OtherTrue() == unrec


def test_unrecognizedunit_eq_delegates_to_other_raises_left():
    """If OtherRaises.__eq__ raises, that exception should propagate when comparing UnrecognizedUnit == OtherRaises()."""
    unrec = u.Unit("FOO", parse_strict='silent')
    with pytest.raises(RuntimeError, match="other_eq_called"):
        _ = (unrec == OtherRaises())


def test_unrecognizedunit_eq_delegates_to_other_raises_right():
    """If OtherRaises.__eq__ raises, that exception should propagate when comparing OtherRaises() == UnrecognizedUnit."""
    unrec = u.Unit("FOO", parse_strict='silent')
    with pytest.raises(RuntimeError, match="other_eq_called"):
        _ = (OtherRaises() == unrec)


def test_other_in_tuple_with_unit_element():
    """Membership should trigger unit.__eq__ which must return NotImplemented to allow OtherTrue.__eq__ to run."""
    assert OtherTrue() in (u.m,)


def test_other_in_tuple_with_unrecognized_element():
    """Membership when the tuple contains an UnrecognizedUnit should delegate and return True."""
    unrec = u.Unit("FOO", parse_strict='silent')
    assert OtherTrue() in (unrec,)
