from sympy import Symbol, sin, cos, tan, cot, S
from sympy.abc import x
from sympy.simplify.fu import TR5, TR6, TR15, TR16, TR22, _TR56 as T

def test_TR5_pow_flag_symbolic_unchanged():
    k = Symbol('k')
    assert TR5(sin(x) ** k, pow=True) == sin(x) ** k