import pytest
from sympy.core.kind import NumberKind, UndefinedKind
from sympy.core.singleton import S
from sympy.core.symbol import Symbol
from sympy.integrals.integrals import Integral
from sympy.core.function import Derivative
from sympy.matrices import Matrix, MatrixSymbol, MatrixKind, MatMul, SparseMatrix, ImmutableMatrix, ImmutableSparseMatrix
from sympy import Subs, Function, Add, Mul, Tuple
from sympy.tensor.array import Array
comm_x = Symbol('x')
noncomm_x = Symbol('x', commutative=False)