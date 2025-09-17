import pytest
from sympy import Symbol
from sympy.physics.units import meter, second, kilometer, hour, joule, meter as m, kilogram, newton, ampere, coulomb, mole, kelvin
from sympy.physics.units.quantities import Quantity
from sympy.physics.units.systems.si import dimsys_SI
from sympy.physics.units.systems import SI
from sympy.physics.units.definitions.dimension_definitions import length, time, velocity, acceleration, energy, mass, amount_of_substance, temperature, pressure, area
from sympy.physics.units.dimensions import Dimension
from sympy.functions.elementary.exponential import exp
from sympy.core.function import Function
from sympy.core.symbol import symbols
from sympy import Rational