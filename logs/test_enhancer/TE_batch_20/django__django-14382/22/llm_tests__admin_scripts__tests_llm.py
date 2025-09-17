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

import os
import tempfile
from django.test import SimpleTestCase
from django.core.management.templates import TemplateCommand
from django.core.management.base import CommandError

class TemplateCommandTargetValidationTests(SimpleTestCase):

    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmpdir.cleanup)
        self.base = self.tmpdir.name
        self.template_dir = os.path.join(self.base, 'template')
        os.makedirs(self.template_dir)
        with open(os.path.join(self.template_dir, 'app_name.py-tpl'), 'w', encoding='utf-8') as fh:
            fh.write('{{ app_name }}')
        self.apps_dir = os.path.join(self.base, 'apps')
        self.app1_dir = os.path.join(self.apps_dir, 'app1')
        os.makedirs(self.app1_dir)

    def test_trailing_dot(self):
        target = os.path.join(self.app1_dir, '.')
        self._run_handle_and_assert(target, self.app1_dir)

    def test_internal_dot_and_trailing_dot(self):
        target = os.path.join(self.base, 'apps', '.', 'app1', '.')
        self._run_handle_and_assert(target, self.app1_dir)

    def test_multiple_trailing_slashes_and_dot(self):
        target = self.app1_dir + os.sep + '.' + os.sep + os.sep
        self._run_handle_and_assert(target, self.app1_dir)

    def test_mixed_dot_and_dotdot(self):
        complex_path = os.path.join(self.app1_dir, '..', 'app1', '.', '')
        target = complex_path
        self._run_handle_and_assert(target, self.app1_dir)

    def test_relative_leading_dot_with_trailing_dot(self):
        old_cwd = os.getcwd()
        try:
            os.chdir(self.base)
            target = os.path.join('.', 'apps', 'app1', '.')
            self._run_handle_and_assert(target, self.app1_dir)
        finally:
            os.chdir(old_cwd)

    def test_absolute_with_redundant_components(self):
        target = os.path.join(self.base, 'apps', 'app1', '..', 'app1', '.', '')
        self._run_handle_and_assert(target, self.app1_dir)

def test_startapp_target_tilde(self):
    """
    Regression: target='~' should be expanded to the user's home directory
    and its basename validated. Using '~' must not cause a validation error.
    """
    home_dir = os.path.join(self.test_dir, 'home_for_tilde')
    os.makedirs(home_dir)
    with mock.patch.dict(os.environ, {'HOME': home_dir}):
        out, err = self.run_django_admin(['startapp', 'myapp', '~'])
    self.assertNoOutput(err)
    expected_app_path = os.path.join(home_dir, 'myapp', 'apps.py')
    self.assertTrue(os.path.exists(expected_app_path))

def test_startapp_target_tilde_with_trailing_slash(self):
    """
    Regression: target='~/' (trailing slash) should also be handled.
    """
    home_dir = os.path.join(self.test_dir, 'home_for_tilde_slash')
    os.makedirs(home_dir)
    with mock.patch.dict(os.environ, {'HOME': home_dir}):
        out, err = self.run_django_admin(['startapp', 'myapp', '~/'])
    self.assertNoOutput(err)
    expected_app_path = os.path.join(home_dir, 'myapp', 'apps.py')
    self.assertTrue(os.path.exists(expected_app_path))

def test_startapp_target_dot(self):
    """
    Regression: target='.' should be considered as the current working
    directory (resolved to an absolute path) and validated using its basename.
    """
    out, err = self.run_django_admin(['startapp', 'myapp', '.'])
    self.assertNoOutput(err)
    expected_app_path = os.path.join(self.test_dir, 'myapp', 'apps.py')
    self.assertTrue(os.path.exists(expected_app_path))

def test_startapp_target_dot_trailing_slash(self):
    """
    Regression: target='./' (trailing slash) must behave like '.'.
    """
    out, err = self.run_django_admin(['startapp', 'myapp', './'])
    self.assertNoOutput(err)
    expected_app_path = os.path.join(self.test_dir, 'myapp', 'apps.py')
    self.assertTrue(os.path.exists(expected_app_path))

def test_startapp_target_dot_multiple_trailing_slashes(self):
    """
    Regression: target with multiple trailing slashes like './///' should be
    normalized and validated against the absolute directory name.
    """
    target = './' + os.sep * 3
    out, err = self.run_django_admin(['startapp', 'myapp', target])
    self.assertNoOutput(err)
    expected_app_path = os.path.join(self.test_dir, 'myapp', 'apps.py')
    self.assertTrue(os.path.exists(expected_app_path))

def test_startapp_target_current_dir_explicit_path_dot(self):
    """
    Regression: using an explicit '.' path when passed as an absolute-ish
    value should still be accepted after normalization.
    """
    target = os.path.join('.')
    out, err = self.run_django_admin(['startapp', 'myapp', target])
    self.assertNoOutput(err)
    expected_app_path = os.path.join(self.test_dir, 'myapp', 'apps.py')
    self.assertTrue(os.path.exists(expected_app_path))

def test_startapp_target_single_dot_string_multiple_forms(self):
    """
    Regression: various forms that represent the current directory must be
    normalized before validation.
    """
    for t in ('.', './', '././'):
        out, err = self.run_django_admin(['startapp', 'myapp', t])
        self.assertNoOutput(err)
        expected_app_path = os.path.join(self.test_dir, 'myapp', 'apps.py')
        self.assertTrue(os.path.exists(expected_app_path))

def test_startapp_target_tilde_and_dot_combo(self):
    """
    Regression: mixing tilde and relative markers ('~/.') should expand the
    tilde and normalize the path before validation.
    """
    home_dir = os.path.join(self.test_dir, 'home_for_tilde_combo')
    os.makedirs(home_dir)
    subdir = os.path.join(home_dir, 'subdir_for_combo')
    os.makedirs(subdir)
    with mock.patch.dict(os.environ, {'HOME': home_dir}):
        out, err = self.run_django_admin(['startapp', 'myapp', '~/subdir_for_combo/'])
    self.assertNoOutput(err)
    expected_app_path = os.path.join(subdir, 'myapp', 'apps.py')
    self.assertTrue(os.path.exists(expected_app_path))

def test_startapp_target_dot_with_verbose_flag(self):
    """
    Regression: verbose runs shouldn't affect the normalization/validation.
    """
    out, err = self.run_django_admin(['startapp', 'myapp', '.', '--verbosity', '2'])
    self.assertNoOutput(err)
    expected_app_path = os.path.join(self.test_dir, 'myapp', 'apps.py')
    self.assertTrue(os.path.exists(expected_app_path))

def test_startapp_target_tilde_as_home_directory_name_being_identifier(self):
    """
    Regression: when HOME expands to a path whose basename is a valid
    identifier, validation should succeed (covers the common '~' use-case).
    """
    home_dir = os.path.join(self.test_dir, 'home_valid_identifier')
    os.makedirs(home_dir)
    with mock.patch.dict(os.environ, {'HOME': home_dir}):
        out, err = self.run_django_admin(['startapp', 'myapp', '~'])
    self.assertNoOutput(err)
    expected_app_path = os.path.join(home_dir, 'myapp', 'apps.py')
    self.assertTrue(os.path.exists(expected_app_path))

import os
import tempfile
import shutil
from django.core.management.templates import TemplateCommand
from django.core.management import CommandError
import unittest

class TemplateCommandTrailingSlashTests(unittest.TestCase):

    def test_absolute_path_single_trailing_slash(self):
        tmpdir = tempfile.mkdtemp(prefix='test_')
        try:
            target_dir = os.path.join(tmpdir, 'apps', 'app1')
            os.makedirs(target_dir)
            target = target_dir + '/'
            self._run_handle(target)
            self.assertTrue(os.path.exists(target_dir))
        finally:
            shutil.rmtree(tmpdir)

    def test_absolute_path_double_trailing_slash(self):
        tmpdir = tempfile.mkdtemp(prefix='test_')
        try:
            target_dir = os.path.join(tmpdir, 'apps', 'app1')
            os.makedirs(target_dir)
            target = target_dir + '//'
            self._run_handle(target)
            self.assertTrue(os.path.exists(target_dir))
        finally:
            shutil.rmtree(tmpdir)

    def test_absolute_path_triple_trailing_slash(self):
        tmpdir = tempfile.mkdtemp(prefix='test_')
        try:
            target_dir = os.path.join(tmpdir, 'apps', 'app1')
            os.makedirs(target_dir)
            target = target_dir + '///'
            self._run_handle(target)
            self.assertTrue(os.path.exists(target_dir))
        finally:
            shutil.rmtree(tmpdir)

    def test_relative_path_single_trailing_slash(self):
        tmpdir = tempfile.mkdtemp(prefix='test_')
        cwd = os.getcwd()
        try:
            target_dir = os.path.join(tmpdir, 'apps', 'app1')
            os.makedirs(target_dir)
            relpath = os.path.relpath(target_dir, start=cwd)
            target = relpath + '/'
            self._run_handle(target)
            self.assertTrue(os.path.exists(target_dir))
        finally:
            shutil.rmtree(tmpdir)

    def test_relative_path_double_trailing_slash(self):
        tmpdir = tempfile.mkdtemp(prefix='test_')
        cwd = os.getcwd()
        try:
            target_dir = os.path.join(tmpdir, 'apps', 'app1')
            os.makedirs(target_dir)
            relpath = os.path.relpath(target_dir, start=cwd)
            target = relpath + '//'
            self._run_handle(target)
            self.assertTrue(os.path.exists(target_dir))
        finally:
            shutil.rmtree(tmpdir)

    def test_relative_path_with_dot_prefix_and_trailing_slash(self):
        tmpdir = tempfile.mkdtemp(prefix='test_')
        cwd = os.getcwd()
        try:
            target_dir = os.path.join(tmpdir, 'apps', 'app1')
            os.makedirs(target_dir)
            relpath = os.path.relpath(target_dir, start=cwd)
            target = './' + relpath + '/'
            self._run_handle(target)
            self.assertTrue(os.path.exists(target_dir))
        finally:
            shutil.rmtree(tmpdir)

    def test_deep_absolute_path_trailing_slash(self):
        tmpdir = tempfile.mkdtemp(prefix='test_')
        try:
            deep = os.path.join(tmpdir, 'one', 'two', 'three', 'apps', 'app1')
            os.makedirs(deep)
            target = deep + '/'
            self._run_handle(target)
            self.assertTrue(os.path.exists(deep))
        finally:
            shutil.rmtree(tmpdir)

    def test_parent_dir_with_trailing_slash(self):
        tmpdir = tempfile.mkdtemp(prefix='test_')
        try:
            parent = os.path.join(tmpdir, 'parent_dir')
            child = os.path.join(parent, 'apps', 'app1')
            os.makedirs(child)
            target = child + '/'
            self._run_handle(target)
            self.assertTrue(os.path.exists(child))
        finally:
            shutil.rmtree(tmpdir)
if __name__ == '__main__':
    unittest.main()

def test_target_with_parent_segment_relative(self):
    """
    Passing a relative path that ends with '..' should resolve to the parent
    directory and create the app files there.
    """
    apps_dir = os.path.join(self.test_dir, 'apps')
    app1_dir = os.path.join(apps_dir, 'app1')
    os.makedirs(app1_dir)
    out, err = self.run_django_admin(['startapp', 'app', os.path.join('apps', 'app1', '..')])
    self.assertNoOutput(err)
    self.assertTrue(os.path.exists(os.path.join(apps_dir, 'apps.py')))

def test_target_with_parent_segment_relative_trailing_slash(self):
    """
    Same as above, but the target ends with a trailing slash.
    """
    apps_dir = os.path.join(self.test_dir, 'apps')
    app1_dir = os.path.join(apps_dir, 'app1')
    os.makedirs(app1_dir)
    target = os.path.join('apps', 'app1', '..') + os.sep
    out, err = self.run_django_admin(['startapp', 'app', target])
    self.assertNoOutput(err)
    self.assertTrue(os.path.exists(os.path.join(apps_dir, 'apps.py')))

def test_target_with_current_segment_relative(self):
    """
    Passing a relative path that ends with '.' should resolve to the directory
    itself (app1) and create the app files there.
    """
    apps_dir = os.path.join(self.test_dir, 'apps')
    app1_dir = os.path.join(apps_dir, 'app1')
    os.makedirs(app1_dir)
    out, err = self.run_django_admin(['startapp', 'app', os.path.join('apps', 'app1', '.')])
    self.assertNoOutput(err)
    self.assertTrue(os.path.exists(os.path.join(app1_dir, 'apps.py')))

def test_target_with_current_segment_relative_trailing_slash(self):
    """
    Same as above, but the target ends with a trailing slash.
    """
    apps_dir = os.path.join(self.test_dir, 'apps')
    app1_dir = os.path.join(apps_dir, 'app1')
    os.makedirs(app1_dir)
    target = os.path.join('apps', 'app1', '.') + os.sep
    out, err = self.run_django_admin(['startapp', 'app', target])
    self.assertNoOutput(err)
    self.assertTrue(os.path.exists(os.path.join(app1_dir, 'apps.py')))

def test_target_with_parent_segment_absolute(self):
    """
    Absolute path ending with '..' should normalize to the parent directory.
    """
    apps_dir = os.path.join(self.test_dir, 'apps')
    app1_dir = os.path.join(apps_dir, 'app1')
    os.makedirs(app1_dir)
    target_abs = os.path.join(self.test_dir, 'apps', 'app1', '..')
    out, err = self.run_django_admin(['startapp', 'app', target_abs])
    self.assertNoOutput(err)
    self.assertTrue(os.path.exists(os.path.join(apps_dir, 'apps.py')))

def test_target_with_parent_segment_absolute_trailing_slash(self):
    """
    Absolute path ending with '..' and a trailing slash should also normalize.
    """
    apps_dir = os.path.join(self.test_dir, 'apps')
    app1_dir = os.path.join(apps_dir, 'app1')
    os.makedirs(app1_dir)
    target_abs = os.path.join(self.test_dir, 'apps', 'app1', '..') + os.sep
    out, err = self.run_django_admin(['startapp', 'app', target_abs])
    self.assertNoOutput(err)
    self.assertTrue(os.path.exists(os.path.join(apps_dir, 'apps.py')))

def test_target_with_current_segment_absolute(self):
    """
    Absolute path ending with '.' should normalize to the pointed directory.
    """
    apps_dir = os.path.join(self.test_dir, 'apps')
    app1_dir = os.path.join(apps_dir, 'app1')
    os.makedirs(app1_dir)
    target_abs = os.path.join(self.test_dir, 'apps', 'app1', '.')
    out, err = self.run_django_admin(['startapp', 'app', target_abs])
    self.assertNoOutput(err)
    self.assertTrue(os.path.exists(os.path.join(app1_dir, 'apps.py')))

def test_target_with_current_segment_absolute_trailing_slash(self):
    """
    Absolute path ending with './' should normalize as well.
    """
    apps_dir = os.path.join(self.test_dir, 'apps')
    app1_dir = os.path.join(apps_dir, 'app1')
    os.makedirs(app1_dir)
    target_abs = os.path.join(self.test_dir, 'apps', 'app1', '.') + os.sep
    out, err = self.run_django_admin(['startapp', 'app', target_abs])
    self.assertNoOutput(err)
    self.assertTrue(os.path.exists(os.path.join(app1_dir, 'apps.py')))

def test_target_with_parent_segment_dot_prefix(self):
    """
    A target prefixed with './' and ending with '..' should still normalize.
    """
    apps_dir = os.path.join(self.test_dir, 'apps')
    app1_dir = os.path.join(apps_dir, 'app1')
    os.makedirs(app1_dir)
    target = os.path.join('.', 'apps', 'app1', '..')
    out, err = self.run_django_admin(['startapp', 'app', target])
    self.assertNoOutput(err)
    self.assertTrue(os.path.exists(os.path.join(apps_dir, 'apps.py')))

def test_target_with_current_segment_dot_prefix(self):
    """
    A target prefixed with './' and ending with '.' should normalize to the directory.
    """
    apps_dir = os.path.join(self.test_dir, 'apps')
    app1_dir = os.path.join(apps_dir, 'app1')
    os.makedirs(app1_dir)
    target = os.path.join('.', 'apps', 'app1', '.')
    out, err = self.run_django_admin(['startapp', 'app', target])
    self.assertNoOutput(err)
    self.assertTrue(os.path.exists(os.path.join(app1_dir, 'apps.py')))

from django.core.management.templates import TemplateCommand
from django.core.management.base import CommandError
import os
import shutil
import tempfile
from django.test import SimpleTestCase
from django.core.management.templates import TemplateCommand
from django.core.management.base import CommandError

class TemplateCommandTargetNormalizationTests(SimpleTestCase):
    """
    Regression tests for validating that TemplateCommand.validate_name()
    checks the basename of the resolved (normalized/absolute) target
    directory (top_dir), not the raw user-supplied target string.

    These tests reproduce paths that include '.' or '..' or trailing
    separators so that a naive basename(target) would be '.' or '..',
    which is not a valid identifier. The correct behavior is to validate
    the basename of the resolved path.
    """

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()

    def test_child_dotdot(self):
        self._run_variant('child/..')

    def test_child_dotdot_with_trailing_slash(self):
        self._run_variant('child/../')

    def test_dot(self):
        self._run_variant('.')

    def test_dot_with_trailing_slash(self):
        self._run_variant('./')

    def test_nested_dot_then_dotdot(self):
        self._run_variant('nested/./..')

    def test_nested_dot_then_dotdot_with_trailing_slash(self):
        self._run_variant('nested/./../')

    def test_child_dot_then_dotdot(self):
        self._run_variant('child/./..')

    def test_parent_reference(self):
        self._run_variant('..')

    def test_parent_reference_with_trailing_slash(self):
        self._run_variant('../')

    def test_multiple_trailing_separators_and_dot(self):
        self._run_variant('./.')