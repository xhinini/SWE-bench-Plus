import pytest
from sympy.core.kind import NumberKind, MatrixKind, UndefinedKind
from sympy.core.singleton import S
from sympy.core.symbol import Symbol
from sympy.integrals.integrals import Integral
from sympy.core.function import Derivative
from sympy import Function
from sympy.matrices import Matrix, MatrixSymbol, ImmutableMatrix
comm_x = Symbol('x')
noncomm_x = Symbol('x', commutative=False)