import pytest
from sympy.core.add import Add
from sympy.core.kind import NumberKind, UndefinedKind
from sympy.core.mul import Mul
from sympy.core.singleton import S
from sympy.core.symbol import Symbol
from sympy.integrals.integrals import Integral
from sympy.core.function import Derivative
from sympy.matrices import Matrix, SparseMatrix, ImmutableMatrix, MatrixSymbol, MatrixKind, MatMul
from sympy import Function
comm_x = Symbol('x')
noncomm_x = Symbol('x', commutative=False)