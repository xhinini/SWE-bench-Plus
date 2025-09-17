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

import ast
from _pytest.assertion.rewrite import rewrite_asserts

def test_integer_constant_not_treated_as_docstring():
    mod = _rewrite_src('0\nother = 1\n')
    _assert_imports_before_constant(mod, 0)

def test_float_constant_not_treated_as_docstring():
    mod = _rewrite_src('3.14159\nother = 1\n')
    _assert_imports_before_constant(mod, 3.14159)

def test_complex_constant_not_treated_as_docstring():
    mod = _rewrite_src('4j\nother = 1\n')
    _assert_imports_before_constant(mod, 4j)

def test_bytes_constant_not_treated_as_docstring():
    mod = _rewrite_src("b'hi'\nother = 1\n")
    _assert_imports_before_constant(mod, b'hi')

def test_empty_bytes_constant_not_treated_as_docstring():
    mod = _rewrite_src("b''\nother = 1\n")
    _assert_imports_before_constant(mod, b'')

def test_true_constant_not_treated_as_docstring():
    mod = _rewrite_src('True\nother = 1\n')
    _assert_imports_before_constant(mod, True)

def test_false_constant_not_treated_as_docstring():
    mod = _rewrite_src('False\nother = 1\n')
    _assert_imports_before_constant(mod, False)

def test_none_constant_not_treated_as_docstring():
    mod = _rewrite_src('None\nother = 1\n')
    _assert_imports_before_constant(mod, None)

def test_ellipses_constant_not_treated_as_docstring():
    mod = _rewrite_src('...\nother = 1\n')
    _assert_imports_before_constant(mod, Ellipsis)

def test_large_int_constant_not_treated_as_docstring():
    val = 123456789012345678901234567890
    mod = _rewrite_src(f'{val}\nother = 1\n')
    _assert_imports_before_constant(mod, val)