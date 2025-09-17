from sympy.physics.units.systems import SI
from sympy.physics.units.quantities import Quantity
from sympy.physics.units.definitions.dimension_definitions import Dimension, length
from sympy.physics.units.definitions import meter
import types
from sympy.physics.units.systems import SI
from sympy.physics.units.quantities import Quantity
from sympy.physics.units.definitions.dimension_definitions import Dimension, length
from sympy.physics.units.definitions import meter

def test_add_equivalent_custom_dimension_should_not_raise():
    q1 = Quantity('q1')
    q2 = Quantity('q2')
    SI.set_quantity_dimension(q1, length)
    q1.set_global_relative_scale_factor(1, meter)
    custom = Dimension('X')
    SI.set_quantity_dimension(q2, custom)
    q2.set_global_relative_scale_factor(1, meter)

    def patch_equiv(self, a, b):
        if a == length and b == custom or (a == custom and b == length):
            return True
        return SI.get_dimension_system().equivalent_dims.__wrapped__(self, a, b) if hasattr(SI.get_dimension_system().equivalent_dims, '__wrapped__') else False

    def patch_getdeps(self, d):
        if d == length:
            return {'L': 1}
        if d == custom:
            return {'X': 1}
        return {}
    ds, restore = _patched_context(patch_equiv, patch_getdeps)
    try:
        val = SI._collect_factor_and_dimension(q1 + q2)
        assert val[0] == 2
        assert val[1] == q1.dimension
    finally:
        restore()

def test_add_three_terms_with_mixed_dimensions_no_error():
    q1 = Quantity('q3a')
    q2 = Quantity('q3b')
    q3 = Quantity('q3c')
    SI.set_quantity_dimension(q1, length)
    SI.set_quantity_dimension(q2, Dimension('A'))
    SI.set_quantity_dimension(q3, Dimension('B'))
    q1.set_global_relative_scale_factor(1, meter)
    q2.set_global_relative_scale_factor(1, meter)
    q3.set_global_relative_scale_factor(1, meter)

    def patch_equiv(self, a, b):
        if a in (length, q2.dimension, q3.dimension) and b in (length, q2.dimension, q3.dimension):
            return True
        return False

    def patch_getdeps(self, d):
        if d == length:
            return {'L': 1}
        if d == q2.dimension:
            return {'A': 1}
        if d == q3.dimension:
            return {'B': 1}
        return {}
    ds, restore = _patched_context(patch_equiv, patch_getdeps)
    try:
        val = SI._collect_factor_and_dimension(q1 + q2 + q3)
        assert val[0] == 3
        assert val[1] == q1.dimension
    finally:
        restore()

def test_nested_add_no_error():
    q1 = Quantity('qn1')
    q2 = Quantity('qn2')
    q3 = Quantity('qn3')
    SI.set_quantity_dimension(q1, length)
    SI.set_quantity_dimension(q2, Dimension('C'))
    SI.set_quantity_dimension(q3, Dimension('D'))
    q1.set_global_relative_scale_factor(1, meter)
    q2.set_global_relative_scale_factor(1, meter)
    q3.set_global_relative_scale_factor(1, meter)

    def patch_equiv(self, a, b):
        if a in (length, q2.dimension, q3.dimension) and b in (length, q2.dimension, q3.dimension):
            return True
        return False

    def patch_getdeps(self, d):
        if d == length:
            return {'L': 1}
        if d == q2.dimension:
            return {'C': 1}
        if d == q3.dimension:
            return {'D': 1}
        return {}
    ds, restore = _patched_context(patch_equiv, patch_getdeps)
    try:
        nested = q1 + q2 + q3
        val = SI._collect_factor_and_dimension(nested)
        assert val[0] == 3
        assert val[1] == q1.dimension
    finally:
        restore()

def test_add_with_nontrivial_dimensions_no_error():
    q1 = Quantity('qt1')
    q2 = Quantity('qt2')
    SI.set_quantity_dimension(q1, length)
    SI.set_quantity_dimension(q2, Dimension('H'))
    q1.set_global_relative_scale_factor(5, meter)
    q2.set_global_relative_scale_factor(7, meter)

    def patch_equiv(self, a, b):
        if a == length and b == q2.dimension or (a == q2.dimension and b == length):
            return True
        return False

    def patch_getdeps(self, d):
        if d == length:
            return {'L': 1}
        if d == q2.dimension:
            return {'H': 1}
        return {}
    ds, restore = _patched_context(patch_equiv, patch_getdeps)
    try:
        expr = 2 * q1 + q2
        val = SI._collect_factor_and_dimension(expr)
        assert val[0] == 17
        assert val[1] == q1.dimension
    finally:
        restore()