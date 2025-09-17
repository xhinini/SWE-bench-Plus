import sys
import types
import pytest
import sys
import types
import pytest
from ..introspection import minversion

def test_minversion_with_postrelease():
    mod = _make_mod('1.2')
    assert minversion(mod, '1.2.post1') is True

def test_minversion_with_local_metadata():
    mod = _make_mod('1.2')
    assert minversion(mod, '1.2+local.1') is True

def test_minversion_with_post_and_local():
    mod = _make_mod('1.2')
    assert minversion(mod, '1.2.post1+build.123') is True

def test_minversion_with_plus_build_only():
    mod = _make_mod('1.2')
    assert minversion(mod, '1.2+build.1') is True

def test_minversion_with_concatenated_post():
    mod = _make_mod('1.2')
    assert minversion(mod, '1.2post1') is True

def test_minversion_with_post_numeric_increment():
    mod = _make_mod('1.2')
    assert minversion(mod, '1.2.post2') is True

def test_minversion_with_local_zero():
    mod = _make_mod('1.2')
    assert minversion(mod, '1.2+0') is True

def test_minversion_with_post_and_dev_combined():
    mod = _make_mod('1.2')
    assert minversion(mod, '1.2.post1.dev0') is True

def test_minversion_accepts_required_with_simple_local():
    mod = _make_mod('1.2')
    assert minversion(mod, '1.2+local') is True

def test_minversion_with_string_module_and_version_path():
    root_name = 'dummy_minversion_mod'
    sub_name = root_name + '.sub'
    root = types.ModuleType(root_name)
    sub = types.ModuleType(sub_name)
    sub.__version__ = '1.2'
    root.sub = sub
    sys.modules[root_name] = root
    sys.modules[sub_name] = sub
    try:
        assert minversion(root_name, '1.2.post1', version_path='sub.__version__') is True
    finally:
        del sys.modules[root_name]
        del sys.modules[sub_name]