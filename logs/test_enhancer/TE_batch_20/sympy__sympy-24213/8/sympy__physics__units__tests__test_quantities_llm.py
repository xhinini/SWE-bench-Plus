import pytest
from sympy import S, Rational
from sympy.core.symbol import Symbol
from sympy.physics.units import meter, second, kilometer, centimeter, amount_of_substance, volume, molar_gas_constant
from sympy.physics.units.quantities import Quantity
from sympy.physics.units.systems import SI
from sympy.physics.units.definitions.dimension_definitions import length, time
from sympy.physics.units.dimensions import Dimension