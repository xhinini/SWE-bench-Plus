import ast
import pytest
from _pytest.assertion.rewrite import rewrite_asserts, AssertionRewriter
from _pytest.assertion.rewrite import _get_assertion_exprs

def test_is_rewrite_disabled_raises_on_none():
    with pytest.raises(TypeError):
        AssertionRewriter.is_rewrite_disabled(None)

def test_is_rewrite_disabled_raises_on_int():
    with pytest.raises(TypeError):
        AssertionRewriter.is_rewrite_disabled(123)

def test_is_rewrite_disabled_raises_on_bytes():
    with pytest.raises(TypeError):
        AssertionRewriter.is_rewrite_disabled(b'PYTEST_DONT_REWRITE')

def test_is_rewrite_disabled_raises_on_ast_constant_object():
    const_node = ast.Constant(value='PYTEST_DONT_REWRITE')
    with pytest.raises(TypeError):
        AssertionRewriter.is_rewrite_disabled(const_node)

def test_run_ignores_numeric_first_expression_and_rewrites_asserts():
    src = '0\n\ndef test_func():\n    assert False\n'
    mod = ast.parse(src)
    rewrite_asserts(mod, src.encode('utf-8'))
    assert isinstance(mod.body[0], ast.Import)
    assert not any((isinstance(n, ast.Assert) for n in ast.walk(mod)))

def test_run_ignores_bytes_first_expression_and_rewrites_asserts():
    src = "b'not a text doc'\n\ndef test_func():\n    assert False\n"
    mod = ast.parse(src)
    rewrite_asserts(mod, src.encode('utf-8'))
    assert isinstance(mod.body[0], ast.Import)
    assert not any((isinstance(n, ast.Assert) for n in ast.walk(mod)))