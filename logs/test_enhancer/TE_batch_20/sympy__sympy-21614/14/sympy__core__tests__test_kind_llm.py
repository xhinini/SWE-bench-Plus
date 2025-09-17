from sympy.core.kind import NumberKind, MatrixKind, UndefinedKind
from sympy.core.singleton import S
from sympy.core.symbol import Symbol
from sympy.matrices import Matrix, MatrixSymbol
from sympy import Integral, Derivative, Function, Subs, sin, diff
from sympy.abc import x, y
comm_x = Symbol('x')
noncomm_x = Symbol('x', commutative=False)