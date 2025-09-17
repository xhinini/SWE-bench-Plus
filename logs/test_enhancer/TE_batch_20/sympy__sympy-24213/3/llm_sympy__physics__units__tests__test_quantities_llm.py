import pytest
from sympy import Rational, Symbol
from sympy.core.numbers import Integer
from sympy.core.singleton import S
from sympy.physics.units import meter, centimeter, second, minute, hour, kilo, kilo as K
from sympy.physics.units import amount_of_substance, volume, molar_gas_constant, joule, meter, second, kilogram, joule as J
from sympy.physics.units.quantities import Quantity
from sympy.physics.units.systems import SI