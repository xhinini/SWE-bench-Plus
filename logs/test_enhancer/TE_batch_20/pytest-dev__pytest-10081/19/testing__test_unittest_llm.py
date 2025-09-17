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