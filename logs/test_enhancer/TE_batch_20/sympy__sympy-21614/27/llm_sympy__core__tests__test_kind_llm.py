import pytest
from sympy import symbols, Function, Subs, Derivative, Matrix, ImmutableMatrix
from sympy import MatrixSymbol, Tuple, Array
from sympy.core.symbol import Symbol
from sympy.core.kind import NumberKind, UndefinedKind, MatrixKind
from sympy.core.singleton import S
from sympy.matrices import MatMul
from sympy.tensor.array.array_derivatives import ArrayDerivative
from sympy.abc import x, y