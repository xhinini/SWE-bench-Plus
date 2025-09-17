import pytest
from sympy import Rational, Symbol
from sympy.physics.units import meter, second, centimeter, kilometer, hour, minute, Quantity
from sympy.physics.units.systems import SI
from sympy.physics.units.definitions.dimension_definitions import length, time, Dimension
from sympy.physics.units import convert_to, PREFIXES
from sympy.core.numbers import Integer