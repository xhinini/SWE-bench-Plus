import pytest
from sympy.core.kind import NumberKind
from sympy.core.kind import UndefinedKind
from sympy.core.singleton import S
from sympy.core.symbol import Symbol
from sympy.integrals.integrals import Integral
from sympy.core.function import Derivative
from sympy.core.add import Add
from sympy.core.mul import Mul
from sympy.matrices import Matrix, SparseMatrix, ImmutableMatrix, ImmutableSparseMatrix, MatrixSymbol, MatrixKind, MatMul, MatAdd
from sympy import Function, Subs, Tuple
comm_x = Symbol('x')
noncomm_x = Symbol('x', commutative=False)