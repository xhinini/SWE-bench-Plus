from sympy.core.compatibility import exec_
from typing import Any, Dict
from sympy.printing import srepr
from sympy import Integer
from sympy.abc import x
from sympy.core.compatibility import exec_
from typing import Any, Dict
ENV: Dict[str, Any] = {}
exec_('from sympy import *', ENV)