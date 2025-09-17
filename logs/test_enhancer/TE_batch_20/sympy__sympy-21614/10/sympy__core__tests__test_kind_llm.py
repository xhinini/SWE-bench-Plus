import pytest
from sympy.core.kind import NumberKind, UndefinedKind
from sympy.matrices import Matrix, MatrixSymbol, MatrixKind
from sympy.core.symbol import Symbol
from sympy.core.singleton import S
from sympy.core.function import Derivative
from sympy import Function, Subs, Lambda, sin
x, y = (Symbol('x'), Symbol('y'))