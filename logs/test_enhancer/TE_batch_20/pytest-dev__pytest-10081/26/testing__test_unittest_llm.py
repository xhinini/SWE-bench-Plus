import inspect
import ast
import _pytest.unittest as ut
import pytest
from typing import Optional

def test_assert_isinstance_parent_unit_testcase_present():
    src, _ = _get_source_and_tree()
    assert 'assert isinstance(self.parent, UnitTestCase)' in src

def test_skipped_assignment_present():
    src, _ = _get_source_and_tree()
    assert 'skipped = _is_skipped(self.obj) or _is_skipped(self.parent.obj)' in src

def test_if_uses_not_skipped_variable():
    src, _ = _get_source_and_tree()
    assert 'if self.config.getoption("usepdb") and not skipped' in src

def test_assert_comes_before_skipped_assignment():
    src, _ = _get_source_and_tree()
    ai = src.find('assert isinstance(self.parent, UnitTestCase)')
    si = src.find('skipped = _is_skipped(self.obj) or _is_skipped(self.parent.obj)')
    assert ai != -1 and si != -1 and (ai < si)

def test_ast_contains_assert_isinstance_of_parent_unit_testcase():
    _, tree = _get_source_and_tree()
    found = False
    for node in ast.walk(tree):
        if isinstance(node, ast.Assert):
            test = node.test
            if isinstance(test, ast.Call) and getattr(test.func, 'id', None) == 'isinstance' and (len(test.args) == 2):
                left, right = test.args
                if isinstance(left, ast.Attribute) and isinstance(left.value, ast.Attribute) and isinstance(left.value.value, ast.Name) and (left.value.value.id == 'self') and (left.value.attr == 'parent') and (left.attr == 'obj') or left.attr == 'parent':
                    if isinstance(right, ast.Name) and right.id == 'UnitTestCase':
                        found = True
                        break
    assert found, 'Expected assert isinstance(self.parent, UnitTestCase) in runtest'

def test_if_node_uses_not_skipped_name_instead_of_inlined_calls():
    _, tree = _get_source_and_tree()
    found = False
    for node in ast.walk(tree):
        if isinstance(node, ast.If):
            test = node.test
            if isinstance(test, ast.BoolOp) and isinstance(test.op, ast.And):
                if len(test.values) >= 2:
                    second = test.values[1]
                    if isinstance(second, ast.UnaryOp) and isinstance(second.op, ast.Not) and isinstance(second.operand, ast.Name) and (second.operand.id == 'skipped'):
                        found = True
                        break
    assert found, "Expected an if-check using 'not skipped' (not an inlined _is_skipped(...) ored expression)"

def test_skipped_assignment_occurs_only_once():
    src, _ = _get_source_and_tree()
    cnt = src.count('skipped = _is_skipped(self.obj) or _is_skipped(self.parent.obj)')
    assert cnt == 1, f"Expected exactly one 'skipped' assignment, found {cnt}"

def test_no_inlined_parent_skip_check_in_if():
    src, _ = _get_source_and_tree()
    inlined_pattern = 'if self.config.getoption("usepdb") and not (_is_skipped(self.obj) or _is_skipped(self.parent.obj))'
    assert inlined_pattern not in src

import types
import unittest
import pytest
import types
import unittest
import pytest

def test_dummy_parent_causes_assertion_basic(pytester):
    source = '\n    import unittest\n    class MyTestCase(unittest.TestCase):\n        def test_foo(self):\n            pass\n    '
    item = _prepare_item_for_runtest_with_dummy_parent(pytester, source)
    with pytest.raises(AssertionError):
        item.runtest()

def test_dummy_parent_with_method_skip_decorator(pytester):
    source = '\n    import unittest\n    class MyTestCase(unittest.TestCase):\n        @unittest.skip("skip me")\n        def test_foo(self):\n            pass\n    '
    item = _prepare_item_for_runtest_with_dummy_parent(pytester, source)
    with pytest.raises(AssertionError):
        item.runtest()

def test_dummy_parent_with_class_skip_decorator(pytester):
    source = '\n    import unittest\n    @unittest.skip("skip class")\n    class MyTestCase(unittest.TestCase):\n        def test_foo(self):\n            pass\n    '
    item = _prepare_item_for_runtest_with_dummy_parent(pytester, source)
    with pytest.raises(AssertionError):
        item.runtest()

def test_dummy_parent_with_method__unittest_skip_attr(pytester):
    source = '\n    import unittest\n    class MyTestCase(unittest.TestCase):\n        def test_foo(self):\n            pass\n    '
    item = _prepare_item_for_runtest_with_dummy_parent(pytester, source)
    try:
        setattr(item.obj.__func__, '__unittest_skip__', True)
    except Exception:
        setattr(item.obj, '__unittest_skip__', True)
    with pytest.raises(AssertionError):
        item.runtest()

def test_dummy_parent_with_class__unittest_skip_attr(pytester):
    source = '\n    import unittest\n    class MyTestCase(unittest.TestCase):\n        __unittest_skip__ = True\n        def test_foo(self):\n            pass\n    '
    item = _prepare_item_for_runtest_with_dummy_parent(pytester, source)
    with pytest.raises(AssertionError):
        item.runtest()

def test_dummy_parent_obj_is_instance_not_class(pytester):
    source = '\n    import unittest\n    class MyTestCase(unittest.TestCase):\n        def test_foo(self):\n            pass\n    '
    item, = pytester.getitems(source)
    item.config.option.usepdb = True
    cls = item.parent.obj
    dummy_parent = types.SimpleNamespace(obj=cls(item.name))
    item.parent = dummy_parent
    item._testcase = cls(item.name)
    item.obj = getattr(item._testcase, item.name)
    with pytest.raises(AssertionError):
        item.runtest()

def test_dummy_parent_multiple_tests_consistency(pytester):
    source = '\n    import unittest\n    class MyTestCase(unittest.TestCase):\n        def test_a(self):\n            pass\n        def test_b(self):\n            pass\n    '
    items = pytester.getitems(source)
    for item in items:
        item.config.option.usepdb = True
        cls = item.parent.obj
        item.parent = types.SimpleNamespace(obj=cls)
        item._testcase = cls(item.name)
        item.obj = getattr(item._testcase, item.name)
        with pytest.raises(AssertionError):
            item.runtest()

def test_dummy_parent_when_bound_method_wrapped(pytester, monkeypatch):
    source = '\n    import unittest\n    class MyTestCase(unittest.TestCase):\n        def test_foo(self):\n            pass\n    '
    item = _prepare_item_for_runtest_with_dummy_parent(pytester, source)
    orig = item.obj

    def wrapper(*args, **kwargs):
        return orig(*args, **kwargs)
    item.obj = wrapper
    item.config.option.usepdb = True
    with pytest.raises(AssertionError):
        item.runtest()