import pytest
from sympy import symbols, Integer
from sympy.physics.quantum.tensorproduct import TensorProduct as TP
A, B, C, D = symbols('A B C D', commutative=False)
x = symbols('x')