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