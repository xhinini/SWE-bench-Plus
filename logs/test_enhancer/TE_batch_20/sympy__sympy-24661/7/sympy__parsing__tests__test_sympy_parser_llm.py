import pytest
from sympy import Lt, Le, Gt, Ge, Ne, Eq, And, Integer, Symbol, sin, Function
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, convert_equals_signs