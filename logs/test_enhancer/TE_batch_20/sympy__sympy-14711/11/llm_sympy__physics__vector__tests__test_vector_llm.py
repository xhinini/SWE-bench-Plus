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

from sympy import ImmutableMatrix as Matrix
from sympy.physics.vector import ReferenceFrame, Vector
from sympy.physics.vector.vector import _check_vector
from sympy.utilities.pytest import raises
Vector.simp = True
A = ReferenceFrame('A')

def test_check_vector_rejects_plain_zero():
    raises(TypeError, lambda: _check_vector(0))

def test_dot_rejects_plain_zero():
    raises(TypeError, lambda: A.x & 0)

def test_outer_rejects_plain_zero():
    raises(TypeError, lambda: A.x | 0)

def test_cross_rejects_plain_zero():
    raises(TypeError, lambda: A.x ^ 0)

from sympy import S
from sympy import S
from sympy.physics.vector import ReferenceFrame
from sympy.utilities.pytest import raises

def test_dot_with_int_zero_left():
    N = ReferenceFrame('N')
    v = N.x
    raises(TypeError, lambda: v & 0)

def test_dot_with_int_zero_right():
    N = ReferenceFrame('N')
    v = N.x
    raises(TypeError, lambda: 0 & v)

def test_cross_with_int_zero_left():
    N = ReferenceFrame('N')
    v = N.x
    raises(TypeError, lambda: v ^ 0)

def test_outer_with_int_zero_left():
    N = ReferenceFrame('N')
    v = N.x
    raises(TypeError, lambda: v | 0)

def test_outer_with_int_zero_right():
    N = ReferenceFrame('N')
    v = N.x
    raises(TypeError, lambda: 0 | v)

def test_dot_with_sympy_zero():
    N = ReferenceFrame('N')
    v = N.x
    raises(TypeError, lambda: v & S.Zero)

def test_cross_with_sympy_zero():
    N = ReferenceFrame('N')
    v = N.x
    raises(TypeError, lambda: v ^ S.Zero)

def test_outer_with_sympy_zero():
    N = ReferenceFrame('N')
    v = N.x
    raises(TypeError, lambda: v | S.Zero)

from sympy.physics.vector import ReferenceFrame, Vector
from sympy.utilities.pytest import raises
from sympy.physics.vector import ReferenceFrame, Vector
from sympy.utilities.pytest import raises
A = ReferenceFrame('A')

def test_dot_with_zero_raises_left_vector():
    raises(TypeError, lambda: A.x & 0)

def test_dot_with_zero_raises_right_vector():
    raises(TypeError, lambda: 0 & A.x)

def test_outer_with_zero_raises_left_vector():
    raises(TypeError, lambda: A.x | 0)

def test_outer_with_zero_raises_right_vector():
    raises(TypeError, lambda: 0 | A.x)

def test_cross_with_zero_raises_left_vector():
    raises(TypeError, lambda: A.x ^ 0)

def test_dot_method_with_zero_raises():
    raises(TypeError, lambda: A.x.dot(0))

def test_outer_method_with_zero_raises():
    raises(TypeError, lambda: A.x.outer(0))

def test_cross_method_with_zero_raises():
    raises(TypeError, lambda: A.x.cross(0))

from sympy import symbols
from sympy.physics.vector import ReferenceFrame, Vector
from sympy.utilities.pytest import raises

def test_dot_with_plain_zero_raises_TypeError():
    N = ReferenceFrame('N')
    raises(TypeError, lambda: N.x & 0)
    assert N.x & Vector(0) == 0

def test_outer_with_plain_zero_raises_TypeError():
    N = ReferenceFrame('N')
    raises(TypeError, lambda: N.x | 0)

def test_cross_with_plain_zero_raises_TypeError():
    N = ReferenceFrame('N')
    raises(TypeError, lambda: N.x ^ 0)

from sympy.utilities.pytest import raises
from sympy.physics.vector import ReferenceFrame, Vector
from sympy.physics.vector.vector import _check_vector

def test_check_vector_rejects_zero():
    raises(TypeError, lambda: _check_vector(0))

def test_and_with_zero_rhs_raises():
    N = ReferenceFrame('N_and_rhs')
    raises(TypeError, lambda: N.x & 0)

def test_and_with_zero_lhs_raises():
    N = ReferenceFrame('N_and_lhs')
    raises(TypeError, lambda: 0 & N.x)

def test_and_direct_method_call_with_zero_raises():
    N = ReferenceFrame('N_and_direct')
    raises(TypeError, lambda: N.x.__and__(0))

def test_or_with_zero_rhs_raises():
    N = ReferenceFrame('N_or_rhs')
    raises(TypeError, lambda: N.x | 0)

def test_or_with_zero_lhs_raises():
    N = ReferenceFrame('N_or_lhs')
    raises(TypeError, lambda: 0 | N.x)

def test_or_direct_method_call_with_zero_raises():
    N = ReferenceFrame('N_or_direct')
    raises(TypeError, lambda: N.x.__or__(0))

def test_ror_direct_method_with_zero_raises():
    N = ReferenceFrame('N_ror_direct')
    raises(TypeError, lambda: N.x.__ror__(0))

def test_xor_with_zero_rhs_raises():
    N = ReferenceFrame('N_xor_rhs')
    raises(TypeError, lambda: N.x ^ 0)