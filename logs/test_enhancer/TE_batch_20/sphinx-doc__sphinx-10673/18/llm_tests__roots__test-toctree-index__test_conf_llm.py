from types import SimpleNamespace
import importlib
import pytest
import types
import builtins
import inspect
import importlib
from types import SimpleNamespace
import pytest
other = importlib.import_module('sphinx.directives.other')
TocTree = other.TocTree
addnodes = importlib.import_module('sphinx.addnodes')