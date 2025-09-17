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