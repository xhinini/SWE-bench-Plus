from sympy.physics.vector import ReferenceFrame, Vector
from sympy.physics.vector.dyadic import Dyadic
from sympy.physics.vector.vector import _check_vector
from sympy.utilities.pytest import raises
N = ReferenceFrame('N')

def test_dot_with_zero_raises_type_error_left():
    raises(TypeError, lambda: N.x & 0)

def test_dot_with_zero_raises_type_error_right():
    raises(TypeError, lambda: 0 & N.x)

def test_outer_with_zero_raises_type_error_left():
    raises(TypeError, lambda: N.x | 0)

def test_outer_with_zero_raises_type_error_right():
    raises(TypeError, lambda: 0 | N.x)

def test_cross_with_zero_raises_type_error():
    raises(TypeError, lambda: N.x ^ 0)

def test_private_check_vector_raises_on_zero():
    raises(TypeError, lambda: _check_vector(0))

from sympy.physics.vector import ReferenceFrame, Vector
from sympy.utilities.pytest import raises
Vector.simp = True
A = ReferenceFrame('A')

def test_dot_with_int_zero_raises_typeerror_right():
    raises(TypeError, lambda: A.x & 0)

def test_dot_with_int_zero_raises_typeerror_via_dunder():
    raises(TypeError, lambda: Vector.__and__(A.x, 0))

def test_dot_with_float_zero_raises_typeerror():
    raises(TypeError, lambda: A.x & 0.0)

def test_cross_with_int_zero_raises_typeerror_right():
    raises(TypeError, lambda: A.x ^ 0)

def test_cross_with_float_zero_raises_typeerror():
    raises(TypeError, lambda: Vector.__xor__(A.x, 0.0))

def test_outer_with_int_zero_raises_typeerror_right():
    raises(TypeError, lambda: A.x | 0)

def test_outer_dunder_ror_with_int_zero_raises_typeerror():
    raises(TypeError, lambda: Vector.__ror__(A.x, 0))

from sympy import symbols, cos
from sympy import ImmutableMatrix as Matrix
from sympy.physics.vector import ReferenceFrame, Vector
from sympy.utilities.pytest import raises
from sympy import symbols, cos
from sympy import ImmutableMatrix as Matrix
from sympy.physics.vector import ReferenceFrame, Vector
from sympy.utilities.pytest import raises

def test_dot_with_zero_raises_typeerror():
    R = ReferenceFrame('R')
    raises(TypeError, lambda: R.x & 0)

def test_outer_with_zero_raises_typeerror():
    R = ReferenceFrame('R')
    raises(TypeError, lambda: 0 | R.x)