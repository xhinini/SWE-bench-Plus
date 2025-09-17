import pytest
from sympy.core.kind import NumberKind
from sympy.core.singleton import S
from sympy.core.symbol import Symbol
from sympy.core.function import Derivative
from sympy.core.add import Add
from sympy.core.mul import Mul
from sympy.core.numbers import pi, I
from sympy.matrices import Matrix, SparseMatrix, ImmutableMatrix, ImmutableSparseMatrix, MatrixSymbol, MatrixKind, MatMul
from sympy import Tuple as SymTuple
x = Symbol('x')
y = Symbol('y')