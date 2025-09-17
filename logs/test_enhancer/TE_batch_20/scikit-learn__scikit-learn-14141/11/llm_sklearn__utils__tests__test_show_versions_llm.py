import sys
import importlib
import types
import pytest
from sklearn.utils._show_versions import _get_sys_info, _get_deps_info, _get_blas_info, show_versions