from sympy import Rational, symbols
from sympy.core.function import Function
from sympy.functions.elementary.exponential import exp, log
from sympy.physics.units import meter, second
from sympy.physics.units.definitions.dimension_definitions import Dimension, length, time, amount_of_substance, volume
from sympy.physics.units.quantities import Quantity
from sympy.physics.units.systems import SI

def test_exp_length_over_time_returns_length_div_time_dimension():
    v = Quantity('v_len')
    t = Quantity('t_time')
    v.set_global_relative_scale_factor(1, meter)
    t.set_global_relative_scale_factor(1, second)
    res = SI._collect_factor_and_dimension(exp(v / t))
    assert isinstance(res, tuple)
    assert res[1] == length / time

def test_exp_of_product_preserves_product_dimension():
    q1 = Quantity('q1')
    q2 = Quantity('q2')
    q1.set_global_relative_scale_factor(1, meter)
    q2.set_global_relative_scale_factor(1, second)
    res = SI._collect_factor_and_dimension(exp(q1 * q2))
    assert isinstance(res, tuple)
    assert res[1] == length * time

def test_exp_of_sum_of_same_dimension_does_not_raise_and_preserves_dimension():
    a = Quantity('a')
    b = Quantity('b')
    a.set_global_relative_scale_factor(2, meter)
    b.set_global_relative_scale_factor(3, meter)
    s = a + b
    res = SI._collect_factor_and_dimension(exp(s))
    assert isinstance(res, tuple)
    assert res[1] == length

def test_exp_of_derivative_expression_preserves_dimension():
    x = symbols('x')
    l = Quantity('Lq')
    t = Quantity('Tq')
    l.set_global_relative_scale_factor(36, meter)
    t.set_global_relative_scale_factor(1, second)
    f = Function('f')
    dfdx = f(x).diff(x)
    dl_dt = dfdx.subs({f(x): l, x: t})
    res = SI._collect_factor_and_dimension(exp(dl_dt))
    assert isinstance(res, tuple)
    assert res[1] == length / time