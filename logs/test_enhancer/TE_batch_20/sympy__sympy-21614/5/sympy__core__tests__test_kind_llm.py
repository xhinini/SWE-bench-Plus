from sympy.core.add import Add
from sympy.core.mul import Mul
from sympy.matrices import MatrixSymbol, MatMul, MatrixKind
from sympy.core.symbol import Symbol
from sympy.core.singleton import S
from sympy import Function, Derivative, Integral, Subs
comm_x = Symbol('x')
noncomm_x = Symbol('x', commutative=False)