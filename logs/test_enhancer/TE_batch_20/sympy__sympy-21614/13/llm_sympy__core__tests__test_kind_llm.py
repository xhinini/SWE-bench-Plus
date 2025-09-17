from sympy import Function, Matrix
from sympy.core.kind import NumberKind, MatrixKind
from sympy.core.symbol import Symbol
from sympy.core.function import Derivative
from sympy.matrices import SparseMatrix, ImmutableMatrix, ImmutableSparseMatrix, MatrixSymbol, MatMul
from sympy.integrals.integrals import Integral
comm_x = Symbol('x')
A = MatrixSymbol('A', 2, 2)
M = Matrix([[1, 2], [3, 4]])
matrix_classes = (Matrix, SparseMatrix, ImmutableMatrix, ImmutableSparseMatrix)