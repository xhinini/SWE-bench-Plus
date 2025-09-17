import pytest
from sympy.core.kind import NumberKind
from sympy.core.function import Derivative
from sympy.core.symbol import Symbol
from sympy.core.singleton import S
from sympy.core.function import Subs, Lambda
from sympy import Function, MatMul
from sympy.matrices import Matrix, MatrixSymbol, MatrixKind, ImmutableMatrix, SparseMatrix, ImmutableSparseMatrix
comm_x = Symbol('x')
noncomm_x = Symbol('x', commutative=False)