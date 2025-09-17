from sympy import symbols
from sympy.functions import Min, Max
from sympy.printing.pycode import PythonCodePrinter, MpmathPrinter, SymPyPrinter, pycode
x, y = symbols('x y')

def test_class_kf_python_contains_min_max():
    assert 'Min' in PythonCodePrinter._kf, "PythonCodePrinter._kf must contain 'Min'"
    assert 'Max' in PythonCodePrinter._kf, "PythonCodePrinter._kf must contain 'Max'"
    assert PythonCodePrinter._kf['Min'] == 'min'
    assert PythonCodePrinter._kf['Max'] == 'max'

def test_instance_known_functions_python_contains_min_max():
    p = PythonCodePrinter()
    assert 'Min' in p.known_functions
    assert 'Max' in p.known_functions
    assert p.known_functions['Min'] == 'min'
    assert p.known_functions['Max'] == 'max'

def test_class_kf_mpmath_contains_min_max():
    assert 'Min' in MpmathPrinter._kf, "MpmathPrinter._kf must contain 'Min'"
    assert 'Max' in MpmathPrinter._kf, "MpmathPrinter._kf must contain 'Max'"
    assert MpmathPrinter._kf['Min'] == 'min'
    assert MpmathPrinter._kf['Max'] == 'max'

def test_instance_known_functions_mpmath_contains_min_max():
    p = MpmathPrinter()
    assert 'Min' in p.known_functions
    assert 'Max' in p.known_functions
    assert p.known_functions['Min'] == 'min'
    assert p.known_functions['Max'] == 'max'

def test_instance_known_functions_sympy_contains_min_max():
    p = SymPyPrinter()
    assert 'Min' in p.known_functions
    assert 'Max' in p.known_functions
    assert p.known_functions['Min'] == 'min'
    assert p.known_functions['Max'] == 'max'

def test_print_sympy_min_max_two_args():
    p = SymPyPrinter()
    assert p.doprint(Min(x, y)) == 'min(x, y)'
    assert p.doprint(Max(x, y)) == 'max(x, y)'