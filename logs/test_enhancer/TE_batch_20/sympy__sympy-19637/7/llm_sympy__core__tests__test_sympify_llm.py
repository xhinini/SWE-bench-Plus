import string
from random import choice
import pytest
from sympy import Symbol, sympify, Integer, Add, Mul, Interval, Function, S, sin, cos
from sympy.abc import x, y
from sympy.core.sympify import kernS, SympifyError