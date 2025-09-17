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

from sympy import Rational
from sympy.functions.elementary.exponential import exp, log
from sympy.functions.elementary.trigonometric import sin
from sympy.physics.units.quantities import Quantity
from sympy.physics.units.systems import SI
from sympy.physics.units.definitions import meter, second
from sympy.physics.units import amount_of_substance, volume
from sympy.physics.units.definitions.dimension_definitions import length, time

def test_exp_of_quantity_returns_factor_and_dimension():
    q = Quantity('q_exp1')
    SI.set_quantity_dimension(q, length)
    q.set_global_relative_scale_factor(3, meter)
    res = SI._collect_factor_and_dimension(exp(q))
    assert res[0] == exp(3)
    assert res[1] == length

def test_exp_of_two_times_quantity_preserves_dimension():
    q = Quantity('q_exp2')
    SI.set_quantity_dimension(q, length)
    q.set_global_relative_scale_factor(4, meter)
    res = SI._collect_factor_and_dimension(exp(2 * q))
    assert res[1] == length
    assert res[0] == exp(8)

def test_exp_of_quantity_power_returns_powered_dimension():
    q = Quantity('q_exp3')
    SI.set_quantity_dimension(q, length)
    q.set_global_relative_scale_factor(2, meter)
    res = SI._collect_factor_and_dimension(exp(q ** 2))
    assert res[1] == length ** 2

def test_exp_of_sin_of_quantity_returns_inner_dimension():
    q = Quantity('q_exp4')
    SI.set_quantity_dimension(q, length)
    q.set_global_relative_scale_factor(2, meter)
    res = SI._collect_factor_and_dimension(exp(sin(q)))
    assert res[1] == length

def test_exp_of_quotient_of_quantities_returns_ratio_dimension():
    ql = Quantity('ql')
    qt = Quantity('qt')
    SI.set_quantity_dimension(ql, length)
    SI.set_quantity_dimension(qt, time)
    ql.set_global_relative_scale_factor(5, meter)
    qt.set_global_relative_scale_factor(1, second)
    res = SI._collect_factor_and_dimension(exp(ql / qt))
    assert res[1] == length / time

def test_exp_of_rational_times_quantity_preserves_dimension():
    q = Quantity('q_exp5')
    SI.set_quantity_dimension(q, length)
    q.set_global_relative_scale_factor(7, meter)
    res = SI._collect_factor_and_dimension(exp(Rational(3, 2) * q))
    assert res[1] == length
    assert res[0] == exp(Rational(3, 2) * 7)

def test_exp_of_sum_of_same_dimension_quantities():
    q = Quantity('q_exp7')
    SI.set_quantity_dimension(q, length)
    q.set_global_relative_scale_factor(7, meter)
    res = SI._collect_factor_and_dimension(exp(q + q))
    assert res[1] == length

from sympy.core.singleton import S
from sympy.core.function import Function
from sympy.functions.elementary.exponential import exp, log
from sympy.functions.elementary.complexes import Abs
from sympy.physics.units.quantities import Quantity
from sympy.physics.units.systems import SI
from sympy.physics.units import meter
from sympy.physics.units.definitions.dimension_definitions import volume, amount_of_substance, length, Dimension

def test_regression_nested_exp_preserves_inner_dimension():
    cH, pH = _make_pH()
    collected = SI._collect_factor_and_dimension(exp(exp(pH)))
    assert collected[1] == volume / amount_of_substance