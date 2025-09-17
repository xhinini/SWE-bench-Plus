from sympy import symbols
from sympy.physics.quantum.tensorproduct import TensorProduct, tensor_product_simp
A, B, C, D, E, F, G = symbols('A B C D E F G', commutative=False)
x, y = symbols('x y')