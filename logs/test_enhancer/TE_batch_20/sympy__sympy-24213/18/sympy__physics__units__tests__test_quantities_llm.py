import pytest
from sympy.core.numbers import Rational
from sympy.core.singleton import S
from sympy.core.symbol import symbols
from sympy.physics.units import meter, kilometer, centimeter, second, hour
from sympy.physics.units import meter as m
from sympy.physics.units import kilometer as km
from sympy.physics.units import centimeter as cm
from sympy.physics.units import hour as hr
from sympy.physics.units import length, time, area, volume, energy, mass
from sympy.physics.units.systems.si import SI
from sympy.physics.units.definitions.dimension_definitions import Dimension
from sympy.physics.units.quantities import Quantity
from sympy.testing.pytest import raises