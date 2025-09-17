from types import ModuleType, SimpleNamespace
import importlib
import sys
import pytest
import sys
from types import SimpleNamespace, ModuleType
import importlib
import builtins
import pytest
from sklearn.utils import _show_versions as sv
DEPS_ORDER = ['pip', 'setuptools', 'sklearn', 'numpy', 'scipy', 'Cython', 'pandas', 'matplotlib', 'joblib']