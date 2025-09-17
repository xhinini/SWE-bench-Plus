import os
import os
from .tests import AdminScriptTestCase

class StartAppPathNormalizationTests(AdminScriptTestCase):
    """
    Regression tests for handling target paths containing '.' and '..'
    components. These ensure the command validates the basename of the
    normalized/absolute target (top_dir), not the raw provided target string.
    """

    def _make_dirs(self, *parts):
        path = os.path.join(self.test_dir, *parts)
        os.makedirs(path, exist_ok=True)
        return path

    def test_relative_path_with_trailing_dot(self):
        self._make_dirs('apps', 'app1')
        target = os.path.join('apps', 'app1', '.')
        self._run_and_assert_created(target)

    def test_relative_path_with_leading_dot_slash_and_dot(self):
        self._make_dirs('apps', 'app1')
        target = os.path.join('.', 'apps', 'app1', '.')
        self._run_and_assert_created(target)

    def test_absolute_path_ending_with_dot(self):
        self._make_dirs('apps', 'app1')
        absolute_target = os.path.join(self.test_dir, 'apps', 'app1', '.')
        self._run_and_assert_created(absolute_target)

    def test_path_with_parent_segment_before_dot(self):
        self._make_dirs('apps', 'other')
        self._make_dirs('apps', 'app1')
        target = os.path.join('apps', 'other', '..', 'app1', '.')
        self._run_and_assert_created(target)

    def test_path_with_multiple_redundant_slashes_and_dot(self):
        self._make_dirs('apps', 'app1')
        target = 'apps//app1///.'
        self._run_and_assert_created(target)

    def test_combined_dot_and_parent_segments(self):
        self._make_dirs('apps', 'other')
        self._make_dirs('apps', 'app1')
        target = os.path.join('.', 'apps', 'other', '..', 'app1', '.')
        self._run_and_assert_created(target)

    def test_ends_with_dot_and_slash(self):
        self._make_dirs('apps', 'app1')
        target = os.path.join('apps', 'app1', '.', '')
        self._run_and_assert_created(target)

    def test_multiple_current_dir_components(self):
        self._make_dirs('apps', 'app1')
        target = os.path.join('apps', 'app1', '.', '.', '.')
        self._run_and_assert_created(target)

import os
import shutil
import tempfile
import unittest
from django.core.management.templates import TemplateCommand
import os
import shutil
import tempfile
import unittest
from django.core.management.templates import TemplateCommand
CUSTOM_TEMPLATES_DIR = os.path.join(os.path.dirname(__file__), 'custom_templates')
APP_TEMPLATE = os.path.join(CUSTOM_TEMPLATES_DIR, 'app_template')

class TemplateHandleTargetValidationTests(unittest.TestCase):

    def setUp(self):
        self._tmpdir = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmpdir.cleanup)
        self.orig_cwd = os.getcwd()
        self.addCleanup(lambda: os.chdir(self.orig_cwd))
if __name__ == '__main__':
    unittest.main()

def test_trailing_dot_variant_1(self):
    """startapp accepts a target path that ends with '/.'"""
    app_dir = os.path.join(self.test_dir, 'apps', 'app_dot1')
    os.makedirs(app_dir)
    target = os.path.join('apps', 'app_dot1', '.')
    out, err = self.run_django_admin(['startapp', 'app', target])
    self.assertNoOutput(err)
    self.assertTrue(os.path.exists(os.path.join(app_dir, 'apps.py')))

def test_trailing_dot_variant_2(self):
    """startapp accepts a target path that ends with '/./' (trailing slash after dot)"""
    app_dir = os.path.join(self.test_dir, 'apps', 'app_dot2')
    os.makedirs(app_dir)
    target = os.path.join('apps', 'app_dot2', '.', '')
    out, err = self.run_django_admin(['startapp', 'app', target])
    self.assertNoOutput(err)
    self.assertTrue(os.path.exists(os.path.join(app_dir, 'apps.py')))

def test_trailing_dot_variant_3(self):
    """startapp accepts a target path with multiple './' components at the end"""
    app_dir = os.path.join(self.test_dir, 'apps', 'app_dot3')
    os.makedirs(app_dir)
    target = os.path.join('apps', 'app_dot3', '.', '.', '')
    out, err = self.run_django_admin(['startapp', 'app', target])
    self.assertNoOutput(err)
    self.assertTrue(os.path.exists(os.path.join(app_dir, 'apps.py')))

def test_trailing_dot_variant_4(self):
    """startapp accepts a target path prefixed with './' and ending with '/.'"""
    app_dir = os.path.join(self.test_dir, 'apps', 'app_dot4')
    os.makedirs(app_dir)
    target = os.path.join('.', 'apps', 'app_dot4', '.')
    out, err = self.run_django_admin(['startapp', 'app', target])
    self.assertNoOutput(err)
    self.assertTrue(os.path.exists(os.path.join(app_dir, 'apps.py')))

def test_trailing_dot_variant_5(self):
    """startapp accepts a target that contains a parent-directory reference before the final '.'"""
    app_dir = os.path.join(self.test_dir, 'apps', 'app_dot5')
    os.makedirs(app_dir)
    target = os.path.join('apps', 'subdir', '..', 'app_dot5', '.')
    out, err = self.run_django_admin(['startapp', 'app', target])
    self.assertNoOutput(err)
    self.assertTrue(os.path.exists(os.path.join(app_dir, 'apps.py')))

def test_trailing_dot_variant_6(self):
    """startapp accepts a target with doubled separators and ending with '/.'"""
    app_dir = os.path.join(self.test_dir, 'apps', 'app_dot6')
    os.makedirs(app_dir)
    target = 'apps' + os.sep * 2 + 'app_dot6' + os.sep + '.'
    out, err = self.run_django_admin(['startapp', 'app', target])
    self.assertNoOutput(err)
    self.assertTrue(os.path.exists(os.path.join(app_dir, 'apps.py')))

def test_trailing_dot_variant_7(self):
    """startapp accepts a target that has './' in the middle and ends with '/.'"""
    app_dir = os.path.join(self.test_dir, 'apps', 'app_dot7')
    os.makedirs(app_dir)
    target = os.path.join('apps', 'sub', '..', 'app_dot7', '.')
    out, err = self.run_django_admin(['startapp', 'app', target])
    self.assertNoOutput(err)
    self.assertTrue(os.path.exists(os.path.join(app_dir, 'apps.py')))

def test_trailing_dot_variant_8(self):
    """startapp accepts a target with multiple leading './' and trailing '/.'"""
    app_dir = os.path.join(self.test_dir, 'apps', 'app_dot8')
    os.makedirs(app_dir)
    target = os.path.join('.', '.', 'apps', 'app_dot8', '.')
    out, err = self.run_django_admin(['startapp', 'app', target])
    self.assertNoOutput(err)
    self.assertTrue(os.path.exists(os.path.join(app_dir, 'apps.py')))

def test_trailing_dot_variant_9(self):
    """startapp accepts a target with redundant './' elements and trailing '/.'"""
    app_dir = os.path.join(self.test_dir, 'apps', 'app_dot9')
    os.makedirs(app_dir)
    target = os.path.join('apps', '.', 'app_dot9', '.')
    out, err = self.run_django_admin(['startapp', 'app', target])
    self.assertNoOutput(err)
    self.assertTrue(os.path.exists(os.path.join(app_dir, 'apps.py')))

def test_trailing_dot_variant_10(self):
    """startapp accepts a complex target containing './' and '../' components and ending with '/.'"""
    app_dir = os.path.join(self.test_dir, 'apps', 'app_dot10')
    os.makedirs(app_dir)
    target = os.path.join('.', 'apps', 'x', '..', 'app_dot10', '.')
    out, err = self.run_django_admin(['startapp', 'app', target])
    self.assertNoOutput(err)
    self.assertTrue(os.path.exists(os.path.join(app_dir, 'apps.py')))

import os
import shutil
import tempfile
import unittest
from django.core.management.templates import TemplateCommand
from django.core.management import CommandError
import os
import shutil
import tempfile
import unittest
from django.core.management.templates import TemplateCommand
from django.core.management import CommandError

class TemplateHandlePathNormalizationTests(unittest.TestCase):

    def setUp(self):
        self.base_dir = tempfile.mkdtemp(prefix='test_template_base_')

    def tearDown(self):
        shutil.rmtree(self.base_dir, ignore_errors=True)
if __name__ == '__main__':
    unittest.main()

def _ensure_and_run_startapp(self, target):
    """
    Helper to create the resolved top_dir so the command won't fail with
    "Destination directory ... does not exist" and run startapp.
    Returns the resolved absolute top_dir used by the command.
    """
    resolved_top_dir = os.path.abspath(os.path.join(self.test_dir, target))
    os.makedirs(resolved_top_dir, exist_ok=True)
    out, err = self.run_django_admin(['startapp', 'app', target])
    self.assertNoOutput(err)
    self.assertTrue(os.path.exists(os.path.join(resolved_top_dir, 'apps.py')))
    return resolved_top_dir

def test_target_trailing_dot(self):
    """startapp handles a target that ends with '/.'"""
    target = os.path.join('apps', 'app1', '.')
    os.makedirs(os.path.join(self.test_dir, 'apps', 'app1'), exist_ok=True)
    self._ensure_and_run_startapp(target)

def test_target_trailing_dot_slash(self):
    """startapp handles a target that ends with '/./'"""
    target = os.path.join('apps', 'app1', '.', '')
    os.makedirs(os.path.join(self.test_dir, 'apps', 'app1'), exist_ok=True)
    self._ensure_and_run_startapp(target)

def test_target_redundant_slashes_and_dot(self):
    """startapp handles redundant slashes and trailing dot (e.g. 'apps//app1/.')"""
    target = 'apps//app1/.'
    os.makedirs(os.path.join(self.test_dir, 'apps', 'app1'), exist_ok=True)
    self._ensure_and_run_startapp(target)

def test_target_trailing_dotdot(self):
    """startapp handles a target that ends with '/..' (refers to parent directory)"""
    target = os.path.join('apps', 'app1', '..')
    os.makedirs(os.path.join(self.test_dir, 'apps'), exist_ok=True)
    os.makedirs(os.path.join(self.test_dir, 'apps', 'app1'), exist_ok=True)
    resolved = os.path.abspath(os.path.join(self.test_dir, target))
    out, err = self.run_django_admin(['startapp', 'app', target])
    self.assertNoOutput(err)
    self.assertTrue(os.path.exists(os.path.join(resolved, 'apps.py')))

def test_target_trailing_dotdot_with_slash(self):
    """startapp handles a target that ends with '/../' (trailing parent ref)"""
    target = os.path.join('apps', 'app1', '..', '')
    os.makedirs(os.path.join(self.test_dir, 'apps'), exist_ok=True)
    os.makedirs(os.path.join(self.test_dir, 'apps', 'app1'), exist_ok=True)
    resolved = os.path.abspath(os.path.join(self.test_dir, target))
    out, err = self.run_django_admin(['startapp', 'app', target])
    self.assertNoOutput(err)
    self.assertTrue(os.path.exists(os.path.join(resolved, 'apps.py')))

def test_target_absolute_with_trailing_dot(self):
    """startapp handles an absolute path that ends with '/.'"""
    abs_dir = os.path.abspath(os.path.join(self.test_dir, 'apps', 'app1'))
    os.makedirs(abs_dir, exist_ok=True)
    target = abs_dir + os.sep + '.'
    out, err = self.run_django_admin(['startapp', 'app', target])
    self.assertNoOutput(err)
    self.assertTrue(os.path.exists(os.path.join(abs_dir, 'apps.py')))

def test_target_dot_in_middle_with_trailing_dot(self):
    """startapp handles a path that contains './' in the middle and ends with '/.'"""
    target = os.path.join('apps', '.', 'app1', '.')
    os.makedirs(os.path.join(self.test_dir, 'apps', 'app1'), exist_ok=True)
    self._ensure_and_run_startapp(target)

def test_target_repeated_dot_segments(self):
    """startapp handles target containing repeated '././' sequences and trailing dot"""
    target = os.path.join('apps', 'app1', '.', '.', '')
    os.makedirs(os.path.join(self.test_dir, 'apps', 'app1'), exist_ok=True)
    target = os.path.join('apps', 'app1', '.', '.')
    self._ensure_and_run_startapp(target)

def test_target_dotdot_interior_and_trailing_dot(self):
    """startapp handles target with interior '..' followed by trailing '.'"""
    target = os.path.join('apps', 'sub', '..', 'app1', '.')
    os.makedirs(os.path.join(self.test_dir, 'apps', 'app1'), exist_ok=True)
    os.makedirs(os.path.join(self.test_dir, 'apps', 'sub'), exist_ok=True)
    self._ensure_and_run_startapp(target)