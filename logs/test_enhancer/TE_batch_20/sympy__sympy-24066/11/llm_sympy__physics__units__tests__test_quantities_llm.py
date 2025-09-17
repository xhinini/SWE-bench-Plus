import pytest
from sympy import Symbol, Rational
from sympy.functions.elementary.exponential import exp, log
from sympy.core.function import Function
from sympy.physics.units.quantities import Quantity
from sympy.physics.units.systems import SI
from sympy.physics.units import amount_of_substance, volume