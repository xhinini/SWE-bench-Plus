import pytest
from sympy import Symbol, Function, Matrix, ImmutableMatrix, MatrixSymbol, Derivative, Subs, Dummy, Tuple, symbols, diff, sin
from sympy.core.kind import NumberKind, UndefinedKind
from sympy.core.singleton import S
from sympy.matrices import MatrixKind, MatMul
from sympy.tensor.array import NDimArray