from sympy import symbols
from sympy.physics.quantum.tensorproduct import TensorProduct as TP
from sympy.physics.quantum.tensorproduct import TensorProduct
import itertools
A, B, C, D, E, F = symbols('A B C D E F', commutative=False)
x = symbols('x')