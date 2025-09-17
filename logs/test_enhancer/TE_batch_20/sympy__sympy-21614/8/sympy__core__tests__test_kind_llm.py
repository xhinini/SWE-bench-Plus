import pytest
from sympy.core.kind import NumberKind, UndefinedKind
from sympy.core.numbers import pi, zoo, I, AlgebraicNumber
from sympy.core.symbol import Symbol
from sympy.core.function import Derivative
from sympy.matrices import Matrix, MatrixSymbol, MatMul
from sympy.core.singleton import S
comm_x = Symbol('x')
noncomm_x = Symbol('x', commutative=False)