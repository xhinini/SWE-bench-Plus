from sympy.parsing.sympy_parser import parse_expr
from sympy.core import Lt, Le, Gt, Ge, Eq, Ne

def test_chained_lt_becomes_Lt_with_evaluate_false():
    expr = '1 < 2 < 3'
    assert parse_expr(expr, evaluate=False) == Lt(1, 2, evaluate=False)

def test_chained_le_becomes_Le_with_evaluate_false():
    expr = '1 <= 2 <= 3'
    assert parse_expr(expr, evaluate=False) == Le(1, 2, evaluate=False)

def test_chained_gt_becomes_Gt_with_evaluate_false():
    expr = '3 > 2 > 1'
    assert parse_expr(expr, evaluate=False) == Gt(3, 2, evaluate=False)

def test_chained_ge_becomes_Ge_with_evaluate_false():
    expr = '3 >= 2 >= 1'
    assert parse_expr(expr, evaluate=False) == Ge(3, 2, evaluate=False)

def test_chained_eq_becomes_Eq_with_evaluate_false():
    expr = '1 == 2 == 3'
    assert parse_expr(expr, evaluate=False) == Eq(1, 2, evaluate=False)

def test_chained_ne_becomes_Ne_with_evaluate_false():
    expr = '1 != 2 != 3'
    assert parse_expr(expr, evaluate=False) == Ne(1, 2, evaluate=False)

def test_mixed_chain_prefers_first_operator_lt_then_eq():
    expr = '1 < 2 == 2'
    assert parse_expr(expr, evaluate=False) == Lt(1, 2, evaluate=False)

def test_mixed_chain_prefers_first_operator_ge_then_ne():
    expr = '5 >= 4 != 3'
    assert parse_expr(expr, evaluate=False) == Ge(5, 4, evaluate=False)

from sympy.parsing.sympy_parser import parse_expr
from sympy.core import Symbol, Lt, Le, Gt, Ge, Eq, Ne

def test_chained_lt_numeric():
    assert parse_expr('1 < 2 < 3', evaluate=False) == Lt(1, 2, evaluate=False)

def test_chained_le_numeric():
    assert parse_expr('1 <= 2 <= 3', evaluate=False) == Le(1, 2, evaluate=False)

def test_chained_gt_numeric():
    assert parse_expr('3 > 2 > 1', evaluate=False) == Gt(3, 2, evaluate=False)

def test_chained_ge_numeric():
    assert parse_expr('3 >= 2 >= 1', evaluate=False) == Ge(3, 2, evaluate=False)

def test_chained_eq_numeric():
    assert parse_expr('1 == 2 == 3', evaluate=False) == Eq(1, 2, evaluate=False)

def test_chained_ne_numeric():
    assert parse_expr('1 != 2 != 3', evaluate=False) == Ne(1, 2, evaluate=False)

def test_chained_symbols():
    x = Symbol('x')
    y = Symbol('y')
    z = Symbol('z')
    assert parse_expr('x < y < z', evaluate=False) == Lt(x, y, evaluate=False)

def test_mixed_comparisons_first_operator_drives_transformation():
    assert parse_expr('1 < 2 == 3', evaluate=False) == Lt(1, 2, evaluate=False)

def test_chained_comparison_not_boolean():
    res = parse_expr('1 < 2 < 3', evaluate=False)
    assert res is not True and res is not False
    assert isinstance(res, Lt)

from sympy import And
import builtins
import types
from sympy.core import Symbol, Function, Integer
from sympy import And
from sympy.core.relational import Lt, Le, Gt, Ge, Ne, Eq
from sympy.parsing.sympy_parser import parse_expr
from sympy.testing.pytest import raises

def test_multiple_comparisons_chained_evaluate_false_produces_sympy_or_bool():
    res = parse_expr('1 < 2 < 3', evaluate=False)
    assert not isinstance(res, bool)
    assert isinstance(res, (And, Lt, Le, Gt, Ge, Eq, Ne))