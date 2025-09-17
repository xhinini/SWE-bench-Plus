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

from sympy import symbols
from sympy.functions import Min, Max
from sympy.printing.pycode import AbstractPythonCodePrinter, PythonCodePrinter, MpmathPrinter, SymPyPrinter, pycode
x, y = symbols('x y')

def test_abstract_kf_contains_Min():
    assert 'Min' in AbstractPythonCodePrinter._kf

def test_abstract_kf_contains_Max():
    assert 'Max' in AbstractPythonCodePrinter._kf

def test_abstract_kf_maps_to_min_max():
    assert AbstractPythonCodePrinter._kf['Min'] == 'min'
    assert AbstractPythonCodePrinter._kf['Max'] == 'max'

def test_pythonprinter_kf_contains_Min_Max():
    assert 'Min' in PythonCodePrinter._kf
    assert 'Max' in PythonCodePrinter._kf
    assert PythonCodePrinter._kf['Min'] == 'min'
    assert PythonCodePrinter._kf['Max'] == 'max'

def test_pythonprinter_instance_known_functions():
    p = PythonCodePrinter()
    assert 'Min' in p.known_functions
    assert 'Max' in p.known_functions
    assert p.known_functions['Min'] == 'min'
    assert p.known_functions['Max'] == 'max'

def test_mpmathprinter_kf_contains_Min_Max():
    assert 'Min' in MpmathPrinter._kf
    assert 'Max' in MpmathPrinter._kf
    assert MpmathPrinter._kf['Min'] == 'min'
    assert MpmathPrinter._kf['Max'] == 'max'

def test_mpmathprinter_instance_known_functions():
    mp = MpmathPrinter()
    assert 'Min' in mp.known_functions
    assert 'Max' in mp.known_functions
    assert mp.known_functions['Min'] == 'min'
    assert mp.known_functions['Max'] == 'max'

def test_sympyprinter_inherits_kf_entries():
    assert 'Min' in SymPyPrinter._kf
    assert 'Max' in SymPyPrinter._kf
    assert SymPyPrinter._kf['Min'] == 'min'
    assert SymPyPrinter._kf['Max'] == 'max'

from sympy import symbols
from sympy.functions import Min, Max
from sympy.printing.pycode import PythonCodePrinter, MpmathPrinter
x, y, z = symbols('x y z')

def test_user_functions_override_min_simple():
    pr = PythonCodePrinter({'user_functions': {'Min': 'custom_min'}})
    assert pr.doprint(Min(x, y)) == 'custom_min(x, y)'

def test_user_functions_override_max_simple():
    pr = PythonCodePrinter({'user_functions': {'Max': 'custom_max'}})
    assert pr.doprint(Max(x, y)) == 'custom_max(x, y)'

def test_user_functions_override_min_fqmodule_registration():
    pr = PythonCodePrinter({'user_functions': {'Min': 'mymod.custom_min'}})
    assert pr.doprint(Min(x, y)) == 'mymod.custom_min(x, y)'
    assert dict(pr.module_imports) == {'mymod': {'custom_min'}}

def test_user_functions_override_min_fqmodule_unqualified():
    pr = PythonCodePrinter({'fully_qualified_modules': False, 'user_functions': {'Min': 'mymod.custom_min'}})
    assert pr.doprint(Min(x, y)) == 'custom_min(x, y)'

def test_mpmath_printer_user_functions_min():
    p = MpmathPrinter({'user_functions': {'Min': 'mpmath.custom_min'}})
    assert p.doprint(Min(x, y)) == 'mpmath.custom_min(x, y)'
    assert dict(p.module_imports) == {'mpmath': {'custom_min'}}

def test_max_three_arguments_with_user_function():
    pr = PythonCodePrinter({'user_functions': {'Max': 'custom_max'}})
    assert pr.doprint(Max(x, y, z)) == 'custom_max(x, y, z)'

def test_user_functions_override_max_fqmodule_unqualified():
    pr = PythonCodePrinter({'fully_qualified_modules': False, 'user_functions': {'Max': 'mymod.custom_max'}})
    assert pr.doprint(Max(x, y)) == 'custom_max(x, y)'

import sympy.printing.pycode as pycode_mod
from sympy.printing.pycode import AbstractPythonCodePrinter, PythonCodePrinter, MpmathPrinter, SymPyPrinter, pycode
from sympy.printing.numpy import NumPyPrinter
from sympy.functions import Min, Max, acos
from sympy import symbols
x, y = symbols('x y')

def test_abstract_kf_includes_min_max():
    assert 'Min' in AbstractPythonCodePrinter._kf
    assert 'Max' in AbstractPythonCodePrinter._kf

def test_pythonprinter_kf_includes_min_max():
    assert 'Min' in PythonCodePrinter._kf
    assert 'Max' in PythonCodePrinter._kf

def test_mpmathprinter_kf_includes_min_max():
    assert 'Min' in MpmathPrinter._kf
    assert 'Max' in MpmathPrinter._kf

def test_sympyprinter_kf_includes_min_max():
    assert 'Min' in SymPyPrinter._kf
    assert 'Max' in SymPyPrinter._kf

def test_user_functions_override_min_in_mpmath():
    settings = {'user_functions': {'Min': 'my.custom.min'}}
    p = MpmathPrinter(settings)
    assert p.known_functions['Min'] == 'my.custom.min'
    out = p.doprint(Min(x, y))
    assert out == 'my.custom.min(x, y)'
    assert 'my.custom' in p.module_imports
    assert 'min' in p.module_imports['my.custom']

def test_AbstractPythonCodePrinter_kf_has_min_max():
    from sympy.printing.pycode import AbstractPythonCodePrinter
    assert 'Min' in AbstractPythonCodePrinter._kf
    assert 'Max' in AbstractPythonCodePrinter._kf
    assert AbstractPythonCodePrinter._kf['Min'] == 'min'
    assert AbstractPythonCodePrinter._kf['Max'] == 'max'

def test_PythonCodePrinter_kf_has_min_max():
    from sympy.printing.pycode import PythonCodePrinter
    assert 'Min' in PythonCodePrinter._kf
    assert 'Max' in PythonCodePrinter._kf
    assert PythonCodePrinter._kf['Min'] == 'min'
    assert PythonCodePrinter._kf['Max'] == 'max'

def test_MpmathPrinter_kf_has_min_max():
    from sympy.printing.pycode import MpmathPrinter
    assert 'Min' in MpmathPrinter._kf
    assert 'Max' in MpmathPrinter._kf
    assert MpmathPrinter._kf['Min'] == 'min'
    assert MpmathPrinter._kf['Max'] == 'max'

def test_SymPyPrinter_kf_has_min_max():
    from sympy.printing.pycode import SymPyPrinter
    assert 'Min' in SymPyPrinter._kf
    assert 'Max' in SymPyPrinter._kf
    assert SymPyPrinter._kf['Min'] == 'min'
    assert SymPyPrinter._kf['Max'] == 'max'

from sympy import Min, Max, symbols
from sympy.printing.pycode import pycode, PythonCodePrinter, MpmathPrinter
x, y, z = symbols('x y z')

def test_user_functions_override_registers_fqn_and_imports():
    p = PythonCodePrinter({'user_functions': {'Min': 'my.module.min'}})
    out = p.doprint(Min(x, y))
    assert out == 'my.module.min(x, y)'
    assert p.module_imports == {'my.module': {'min'}}

from sympy.functions import Min, Max
from sympy.printing.pycode import MpmathPrinter, PythonCodePrinter, SymPyPrinter
from sympy.printing.numpy import NumPyPrinter, SciPyPrinter

def test_kf_contains_min_max_mpmath():
    assert 'Min' in MpmathPrinter._kf
    assert 'Max' in MpmathPrinter._kf

def test_kf_contains_min_max_pythonprinter():
    assert 'Min' in PythonCodePrinter._kf
    assert 'Max' in PythonCodePrinter._kf

def test_kf_contains_min_max_sympyprinter():
    assert 'Min' in SymPyPrinter._kf
    assert 'Max' in SymPyPrinter._kf

def test_instance_known_functions_mpmath():
    p = MpmathPrinter()
    assert 'Min' in p.known_functions
    assert 'Max' in p.known_functions

def test_instance_known_functions_numpy():
    p = NumPyPrinter()
    assert 'Min' in p.known_functions
    assert 'Max' in p.known_functions

def test_instance_known_functions_scipy():
    p = SciPyPrinter()
    assert 'Min' in p.known_functions
    assert 'Max' in p.known_functions

def test_instance_known_functions_pythonprinter():
    p = PythonCodePrinter()
    assert 'Min' in p.known_functions
    assert 'Max' in p.known_functions

from sympy import Min, Max, symbols
from sympy.printing.pycode import PythonCodePrinter, MpmathPrinter, pycode
x, y, z = symbols('x y z')

def test_min_with_user_function_fully_qualified():
    prntr = PythonCodePrinter({'user_functions': {'Min': 'mymod.min'}})
    assert prntr.doprint(Min(x, y)) == 'mymod.min(x, y)'
    assert prntr.module_imports == {'mymod': {'min'}}

def test_max_with_user_function_fully_qualified():
    prntr = PythonCodePrinter({'user_functions': {'Max': 'mymod.max'}})
    assert prntr.doprint(Max(x, y)) == 'mymod.max(x, y)'
    assert prntr.module_imports == {'mymod': {'max'}}

def test_min_with_fully_qualified_false_still_registers_module():
    prntr = PythonCodePrinter({'user_functions': {'Min': 'mymod.min'}, 'fully_qualified_modules': False})
    assert prntr.doprint(Min(x, y)) == 'min(x, y)'
    assert prntr.module_imports == {'mymod': {'min'}}

def test_numpy_like_user_function_registration():
    prntr = PythonCodePrinter({'user_functions': {'Min': 'numpy.minimum'}})
    assert prntr.doprint(Min(x, y)) == 'numpy.minimum(x, y)'
    assert prntr.module_imports == {'numpy': {'minimum'}}

def test_nested_user_function_mappings():
    prntr = PythonCodePrinter({'user_functions': {'Min': 'pkg.min', 'Max': 'pkg.max'}})
    expr = Min(x, Max(y, z))
    assert prntr.doprint(expr) == 'pkg.min(x, pkg.max(y, z))'
    assert prntr.module_imports == {'pkg': {'min', 'max'}}

def test_pycode_helper_respects_user_functions():
    s = pycode(Min(x, y), user_functions={'Min': 'mymod.min'})
    assert s == 'mymod.min(x, y)'

def test_mpmath_printer_with_user_function():
    p = MpmathPrinter({'user_functions': {'Min': 'mpmath.fmin'}})
    assert p.doprint(Min(x, y)) == 'mpmath.fmin(x, y)'
    assert p.module_imports == {'mpmath': {'fmin'}}