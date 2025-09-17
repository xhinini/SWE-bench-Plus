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