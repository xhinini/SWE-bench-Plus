from sympy import symbols, I
from sympy.physics.quantum.tensorproduct import TensorProduct as TP, tensor_product_simp
from sympy.physics.quantum.tensorproduct import TensorProduct
from sympy import symbols, I
from sympy.core.mul import Mul
from sympy.core.add import Add
from sympy.physics.quantum.tensorproduct import TensorProduct as TP, tensor_product_simp
from sympy.physics.quantum.tensorproduct import TensorProduct
from sympy.physics.quantum.commutator import Commutator as Comm
A, B, C, D, E, F = symbols('A B C D E F', commutative=False)
x, y, z = symbols('x y z')