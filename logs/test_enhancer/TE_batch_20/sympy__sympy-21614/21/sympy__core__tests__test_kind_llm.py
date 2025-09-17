from sympy.core.kind import NumberKind, MatrixKind
from sympy.core.function import Derivative
from sympy.core.symbol import Symbol
from sympy.core.singleton import S
from sympy.matrices import Matrix, SparseMatrix, ImmutableMatrix, ImmutableSparseMatrix, MatrixSymbol, MatMul
from sympy import Function
from sympy.integrals.integrals import Integral
x = Symbol('x')
comm_x = x