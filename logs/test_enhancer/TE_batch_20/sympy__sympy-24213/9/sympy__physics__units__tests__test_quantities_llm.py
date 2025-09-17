import pytest
import pytest
from sympy.core.numbers import Rational
from sympy.core.singleton import S
from sympy.physics.units import meter, second, kilogram, meter as m
from sympy.physics.units import Quantity
from sympy.physics.units.systems import SI
from sympy.physics.units.definitions.dimension_definitions import length, time, mass
from sympy.physics.units.dimensions import Dimension