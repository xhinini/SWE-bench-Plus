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

import ast
from sympy.core import Eq, Ne, Lt, Le, Gt, Ge
from sympy.parsing.sympy_parser import EvaluateFalseTransformer, parse_expr
import ast
from sympy.core import Eq, Ne, Lt, Le, Gt, Ge
from sympy.parsing.sympy_parser import EvaluateFalseTransformer, parse_expr
from sympy.testing.pytest import raises

def test_relational_operators_attribute_exists():
    assert hasattr(EvaluateFalseTransformer, 'relational_operators')

def test_relational_operators_keys_are_expected_ast_classes():
    relops = EvaluateFalseTransformer.relational_operators
    expected = {ast.NotEq, ast.Lt, ast.LtE, ast.Gt, ast.GtE, ast.Eq}
    assert set(relops.keys()) == expected

def test_relational_operators_values_include_Eq_and_Ne():
    relops = EvaluateFalseTransformer.relational_operators
    assert relops[ast.Eq] == 'Eq'
    assert relops[ast.NotEq] == 'Ne'
    assert relops[ast.Lt] == 'Lt'
    assert relops[ast.LtE] == 'Le'
    assert relops[ast.Gt] == 'Gt'
    assert relops[ast.GtE] == 'Ge'

def test_chained_comparisons_are_transformed_to_ast_Call_on_visit():
    module = ast.parse('1 < 2 < 3')
    transformer = EvaluateFalseTransformer()
    new_module = transformer.visit(module)
    assert isinstance(new_module.body[0].value, ast.Call)

from sympy.core import Symbol
from sympy.core import Integer
from sympy.core.relational import Lt, Le, Gt, Ge, Ne, Eq
from sympy.parsing.sympy_parser import parse_expr

def test_chain_lt_numbers():
    res = parse_expr('1 < 2 < 3', evaluate=False)
    assert not isinstance(res, bool)
    assert res == Lt(1, 2, evaluate=False)

def test_chain_le_symbols():
    x = Symbol('x')
    y = Symbol('y')
    z = Symbol('z')
    res = parse_expr('x <= y <= z', evaluate=False)
    assert not isinstance(res, bool)
    assert res == Le(x, y, evaluate=False)

def test_chain_mixed_eq():
    res = parse_expr('1 < 2 == 2', evaluate=False)
    assert not isinstance(res, bool)
    assert res == Lt(1, 2, evaluate=False)

def test_chain_not_eq():
    res = parse_expr('1 != 2 != 3', evaluate=False)
    assert not isinstance(res, bool)
    assert res == Ne(1, 2, evaluate=False)

def test_chain_gt_ge():
    res = parse_expr('5 > 3 >= 2', evaluate=False)
    assert not isinstance(res, bool)
    assert res == Gt(5, 3, evaluate=False)

def test_chain_symbol_number_symbol():
    x = Symbol('x')
    res = parse_expr('x < 2 < 10', evaluate=False)
    assert not isinstance(res, bool)
    assert res == Lt(x, 2, evaluate=False)

def test_chain_long_sequence():
    res = parse_expr('1 < 2 < 3 < 4', evaluate=False)
    assert not isinstance(res, bool)
    assert res == Lt(1, 2, evaluate=False)

def test_chain_first_two_args_preserved():
    res = parse_expr('7 <= 8 <= 9', evaluate=False)
    assert isinstance(res, Le)
    assert res.args[0] == Integer(7)
    assert res.args[1] == Integer(8)