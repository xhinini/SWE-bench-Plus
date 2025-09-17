import pytest
from sympy import Symbol, Rational, exp, sin
from sympy.core.function import Function
from sympy.physics.units import meter, centimeter, millimeter, second, hour, kilo, meter as m_unit, centimeter as cm_unit, amount_of_substance, volume
from sympy.physics.units.quantities import Quantity
from sympy.physics.units.systems import SI
from sympy.physics.units.definitions.dimension_definitions import length, time, area, mass
from sympy.physics.units.definitions import joule
from sympy.physics.units import convert_to