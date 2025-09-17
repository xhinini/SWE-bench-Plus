from sympy import symbols
from sympy.physics.quantum.tensorproduct import TensorProduct as TP, tensor_product_simp
from sympy.physics.quantum.tensorproduct import TensorProduct
from sympy import Integer
A, B, C, D, E, F = symbols('A B C D E F', commutative=False)
x = symbols('x')