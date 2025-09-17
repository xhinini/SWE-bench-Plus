from sympy import Function, Symbol
from sympy.core.kind import NumberKind, UndefinedKind
from sympy.matrices import Matrix, MatrixSymbol, MatrixKind, MatMul
from sympy.core.function import Derivative
from sympy.core.singleton import S
comm_x = Symbol('x')
noncomm_x = Symbol('x', commutative=False)