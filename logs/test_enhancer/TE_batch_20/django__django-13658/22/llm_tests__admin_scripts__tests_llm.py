# No new imports required beyond those used in the test_code.
from django.test import SimpleTestCase
from django.core.management import ManagementUtility, execute_from_command_line

class ManagementUtilityArgvNoneTests(SimpleTestCase):
    def test_instantiation_raises_typeerror_with_list_none(self):
        with self.assertRaises(TypeError):
            # Passing a list where argv[0] is None should raise in the original implementation.
            ManagementUtility(argv=[None])

    def test_instantiation_raises_typeerror_with_list_none_and_help(self):
        with self.assertRaises(TypeError):
            ManagementUtility(argv=[None, 'help'])

    def test_instantiation_raises_typeerror_with_tuple_none(self):
        with self.assertRaises(TypeError):
            # A tuple should behave the same as a list for argv.
            ManagementUtility(argv=(None,))

    def test_instantiation_raises_typeerror_with_tuple_none_and_help(self):
        with self.assertRaises(TypeError):
            ManagementUtility(argv=(None, 'help'))

    def test_execute_from_command_line_raises_with_list_none(self):
        with self.assertRaises(TypeError):
            # execute_from_command_line constructs a ManagementUtility internally.
            execute_from_command_line([None, 'help'])

    def test_execute_from_command_line_raises_with_tuple_none(self):
        with self.assertRaises(TypeError):
            # Passing a tuple-like sequence should also raise.
            execute_from_command_line((None, 'help'))

    def test_execute_method_invocation_raises_with_none_argv0(self):
        with self.assertRaises(TypeError):
            # Attempt to create and execute; instantiation should raise TypeError.
            ManagementUtility(argv=[None, 'help']).execute()

    def test_main_help_text_access_raises_with_none_argv0(self):
        with self.assertRaises(TypeError):
            # Accessing main_help_text requires a valid instance; construction should raise.
            ManagementUtility(argv=[None]).main_help_text()

    def test_autocomplete_path_raises_with_none_argv0(self):
        with self.assertRaises(TypeError):
            # Construction will raise before autocomplete is reachable.
            ManagementUtility(argv=[None, 'help']).autocomplete()

    def test_fetch_command_raises_with_none_argv0(self):
        with self.assertRaises(TypeError):
            # Construction fails, so fetch_command isn't reachable — this ensures the ctor check.
            ManagementUtility(argv=[None, 'help']).fetch_command('help')

from django.core.management import ManagementUtility, execute_from_command_line
from django.test import SimpleTestCase
from django.test.utils import captured_stdout, captured_stderr

class ProgramNameHelpTests(SimpleTestCase):

    def test_execute_from_command_line_with_empty_prog_shows_empty_prog_in_usage(self):
        argv = ['', 'help', 'shell']
        with captured_stdout() as out, captured_stderr() as err:
            execute_from_command_line(argv)
        output = out.getvalue()
        self.assertIn('usage:  shell', output)
        self.assertEqual(err.getvalue(), '')

from unittest import mock
from django.core.management import ManagementUtility
from django.test import SimpleTestCase

class ManagementUtilityProgNameTests(SimpleTestCase):

    def test_prog_name_when_sysargv_empty_string(self):
        with mock.patch('sys.argv', ['']):
            mu = ManagementUtility(argv=[])
            self.assertEqual(mu.prog_name, '')

    def test_prog_name_from_provided_argv_empty_string(self):
        mu = ManagementUtility(argv=[''])
        self.assertEqual(mu.prog_name, '')

# No additional imports required beyond those in the test module.
import os
import sys
import unittest
from unittest import mock

from django.test.utils import captured_stdout, captured_stderr
from django.core.management import ManagementUtility, execute_from_command_line

class ManagementUtilityArgvFalsyTests(unittest.TestCase):
    def test_init_raises_typeerror_on_none_argv0(self):
        # Passing None as argv[0] should raise a TypeError when computing prog_name
        with self.assertRaises(TypeError):
            ManagementUtility([None, 'help'])

    def test_execute_from_command_line_raises_typeerror_when_sys_argv0_is_none(self):
        # When no argv is provided to execute_from_command_line and sys.argv[0] is None,
        # ManagementUtility() should raise a TypeError.
        with mock.patch('sys.argv', [None, 'help']):
            with self.assertRaises(TypeError):
                execute_from_command_line()

    def test_init_raises_typeerror_on_zero_argv0(self):
        # An integer 0 is not a valid path-like object and should raise TypeError.
        with self.assertRaises(TypeError):
            ManagementUtility([0, 'help'])

    def test_init_raises_typeerror_on_false_argv0(self):
        # False (a bool) should also raise TypeError (bool is subclass of int).
        with self.assertRaises(TypeError):
            ManagementUtility([False, 'help'])

    def test_prog_name_is_empty_string_when_argv0_is_empty_string(self):
        # An empty-string argv[0] is valid (it's a string). The prog_name should
        # reflect that empty string (os.path.basename('') == '').
        mu = ManagementUtility(['', 'help'])
        self.assertEqual(mu.prog_name, '')

    def test_execute_from_command_line_reflects_empty_progname_in_usage(self):
        # When execute_from_command_line is given an argv whose first element is '',
        # the usage text should reflect the empty program name.
        args = ['', 'help', 'shell']
        # Ensure sys.argv is different so we validate that the provided argv is used.
        with mock.patch('sys.argv', ['something-else', 'x']), captured_stdout() as out, captured_stderr() as err:
            # execute_from_command_line will use the provided argv argument
            # and should not be influenced by the patched sys.argv.
            execute_from_command_line(args)
        self.assertIn('usage:  shell', out.getvalue())
        self.assertEqual(err.getvalue(), '')

    def test_main_help_text_shows_empty_progname_type_line(self):
        # main_help_text should include the "Type '<prog> help <subcommand>'" line.
        mu = ManagementUtility(['', 'help'])
        text = mu.main_help_text()
        # For empty prog_name, the formatted string will have a leading space before help.
        self.assertIn("Type ' help <subcommand>'", text)

    def test_execute_from_command_line_raises_typeerror_on_int_zero_argv0(self):
        # Calling execute_from_command_line with an argv whose first element is 0
        # should raise TypeError during ManagementUtility initialization.
        with self.assertRaises(TypeError):
            execute_from_command_line([0, 'help'])

    def test_execute_from_command_line_raises_typeerror_on_false_argv0(self):
        # Calling execute_from_command_line with an argv whose first element is False
        # should raise TypeError during ManagementUtility initialization.
        with self.assertRaises(TypeError):
            execute_from_command_line([False, 'help'])

    def test_no_argv_uses_sys_argv_and_raises_if_sys_argv0_is_none(self):
        # Ensure that when no argv is passed, sys.argv is used and causes a TypeError
        # if its first element is None.
        with mock.patch('sys.argv', [None, 'help']):
            with self.assertRaises(TypeError):
                ManagementUtility()  # argv defaults to sys.argv[:]

if __name__ == '__main__':
    unittest.main()

from django.test import SimpleTestCase
from django.core.management import execute_from_command_line
from django.test.utils import captured_stdout, captured_stderr
import os

class ProgramNameHelpTests(SimpleTestCase):
    """
    Regression tests to ensure help and usage text use the program name from
    the argv passed into execute_from_command_line / ManagementUtility.
    These tests cover empty-string program name and __main__.py special case.
    """

    def test_help_subcommand_shows_per_command_usage_with_empty_prog(self):
        with captured_stdout() as out, captured_stderr() as err:
            execute_from_command_line(['', 'help', 'startproject'])
        output = out.getvalue()
        self.assertIn('usage:  startproject', output)

    def test_help_for_specific_command_via_help_subcommand_contains_empty_prog(self):
        with captured_stdout() as out, captured_stderr() as err:
            execute_from_command_line(['', 'help', 'startapp'])
        output = out.getvalue()
        self.assertIn('usage:  startapp', output)

from django.core.management import ManagementUtility, execute_from_command_line
from django.test.utils import captured_stdout
from django.test import SimpleTestCase
from django.core.management import ManagementUtility, execute_from_command_line
from django.test.utils import captured_stdout
import sys

class ManagementUtilityProgNameTests(SimpleTestCase):

    def test_init_raises_typeerror_with_none_argv0(self):
        """
        If argv[0] is None, the original behavior (before a defensive change)
        raises a TypeError when attempting os.path.basename(None). The test
        asserts that a TypeError is raised to detect changes that silently
        accept None and substitute a default program name.
        """
        with self.assertRaises(TypeError):
            ManagementUtility([None, 'help'])

from django.test import SimpleTestCase
from django.core.management import ManagementUtility, execute_from_command_line

class ManagementUtilityArgvNoneTests(SimpleTestCase):
    def test_init_with_argv0_none_raises_typeerror(self):
        """
        Constructing ManagementUtility with argv whose first element is None
        should raise TypeError (os.path.basename(None)).
        """
        with self.assertRaises(TypeError):
            ManagementUtility([None])

    def test_init_with_argv0_none_and_subcommand_raises_typeerror(self):
        """
        Constructing ManagementUtility with argv like [None, 'help'] should
        raise TypeError during initialization.
        """
        with self.assertRaises(TypeError):
            ManagementUtility([None, 'help'])

    def test_execute_from_command_line_with_argv0_none_raises_typeerror(self):
        """
        execute_from_command_line should raise TypeError when given an argv
        list whose first element is None.
        """
        with self.assertRaises(TypeError):
            execute_from_command_line([None, 'help'])

    def test_execute_from_command_line_with_argv0_none_and_more_args_raises_typeerror(self):
        """
        A longer argv list with argv[0] == None should still raise TypeError.
        """
        with self.assertRaises(TypeError):
            execute_from_command_line([None, 'help', 'shell'])

    def test_managementutility_execute_with_argv0_none_raises_typeerror(self):
        """
        Instantiating ManagementUtility with argv[0] None then calling
        execute() should not succeed; the TypeError should be raised on init.
        """
        with self.assertRaises(TypeError):
            mu = ManagementUtility([None, 'help'])
            mu.execute()

    def test_main_help_text_construction_with_argv0_none_raises_typeerror(self):
        """
        Attempting to create a ManagementUtility with argv[0] None and then
        access main_help_text should fail during construction.
        """
        with self.assertRaises(TypeError):
            mu = ManagementUtility([None])
            mu.main_help_text()

    def test_multiple_none_and_values_in_argv_raises_typeerror(self):
        """
        Even if there are many elements, if argv[0] is None a TypeError is
        expected during ManagementUtility construction.
        """
        with self.assertRaises(TypeError):
            ManagementUtility([None, '--settings=test_project.settings', 'check'])

    def test_execute_from_command_line_with_only_none_raises_typeerror(self):
        """
        Passing a single-element argv list with None to execute_from_command_line
        should raise TypeError.
        """
        with self.assertRaises(TypeError):
            execute_from_command_line([None])

    def test_instantiation_then_autocomplete_with_argv0_none_raises_typeerror(self):
        """
        Construction should fail before any method such as autocomplete can be called.
        """
        with self.assertRaises(TypeError):
            mu = ManagementUtility([None, 'help'])
            mu.autocomplete()

    def test_instantiation_with_none_and_empty_string_following_raises_typeerror(self):
        """
        argv like [None, ''] should still raise a TypeError on instantiation.
        """
        with self.assertRaises(TypeError):
            ManagementUtility([None, ''])

from django.core.management import ManagementUtility, execute_from_command_line
from django.test import SimpleTestCase
from django.test.utils import captured_stdout, captured_stderr

class ManagementUtilityInitEdgeCases(SimpleTestCase):

    def test_init_with_none_argv0_raises_typeerror(self):
        """
        If argv[0] is None, the original implementation calls os.path.basename(None)
        which raises a TypeError. The candidate model patch masks this by setting a
        default program name; we assert the original behavior (TypeError) here so
        that the candidate patch is caught.
        """
        with self.assertRaises(TypeError):
            ManagementUtility([None, 'help'])

    def test_execute_with_none_argv0_raises_typeerror(self):
        """
        Ensure constructing and attempting to execute with argv[0] == None raises
        TypeError (raised during initialization). This duplicates the construction
        check but verifies execute() path doesn't unexpectedly swallow it.
        """
        with self.assertRaises(TypeError):
            mu = ManagementUtility([None, 'help'])
            mu.execute()

    def test_execute_from_command_line_empty_argv_usage(self):
        """
        Calling execute_from_command_line with an empty program name should result
        in usage output that includes the empty program name in the usage line
        (i.e. 'usage:  shell' with two spaces before 'shell').
        """
        with captured_stdout() as out, captured_stderr() as err:
            execute_from_command_line(['', 'help', 'shell'])
        self.assertIn('usage:  shell', out.getvalue())

    def test_main_help_text_main_py_shows_python_m(self):
        """
        When argv[0] is '__main__.py', the program name must be converted to
        'python -m django' in help text.
        """
        mu = ManagementUtility(['__main__.py', 'help'])
        text = mu.main_help_text()
        self.assertIn("Type 'python -m django help <subcommand>'", text)

from django.test import SimpleTestCase
from django.test.utils import captured_stdout
from django.core.management import execute_from_command_line, ManagementUtility
import sys
from unittest import mock

class ManagementUtilityProgramNameEdgeCases(SimpleTestCase):
    """
    Tests for edge cases in program name (argv[0]) handling by ManagementUtility
    and execute_from_command_line.
    """

    def test_execute_from_command_line_empty_progname_usage_for_shell(self):
        args = ['help', 'shell']
        with captured_stdout() as out, mock.patch.object(sys, 'argv', ['irrelevant']):
            execute_from_command_line(['', *args])
        output = out.getvalue()
        self.assertIn('usage:  shell', output)

    def test_execute_from_command_line_empty_progname_main_help_text_type_line(self):
        with captured_stdout() as out, mock.patch.object(sys, 'argv', ['irrelevant']):
            execute_from_command_line(['', 'help'])
        output = out.getvalue()
        self.assertIn("Type ' help <subcommand>'", output)

    def test_execute_from_command_line_raises_when_sys_argv0_is_none(self):
        patched = [None, 'help', 'shell']
        with mock.patch('sys.argv', patched):
            with self.assertRaises(TypeError):
                execute_from_command_line()

    def test_management_utility_init_raises_when_sys_argv0_is_none(self):
        patched = [None]
        with mock.patch('sys.argv', patched):
            with self.assertRaises(TypeError):
                ManagementUtility()

    def test_execute_from_command_line_with_sys_argv_none_and_help_flag(self):
        patched = [None, '--help']
        with mock.patch('sys.argv', patched):
            with self.assertRaises(TypeError):
                execute_from_command_line()

    def test_management_utility_init_with_none_and_additional_args_raises(self):
        patched = [None, 'help', 'shell']
        with mock.patch('sys.argv', patched):
            with self.assertRaises(TypeError):
                ManagementUtility()

    def test_execute_from_command_line_empty_progname_and_subcommand_help(self):
        with captured_stdout() as out, mock.patch.object(sys, 'argv', ['irrelevant']):
            execute_from_command_line(['', 'help', 'check'])
        output = out.getvalue()
        self.assertIn('usage:  check', output)

from unittest import mock
from django.core.management import execute_from_command_line, ManagementUtility
from django.test import SimpleTestCase
from django.test.utils import captured_stdout, captured_stderr
from unittest import mock
from django.core.management import execute_from_command_line, ManagementUtility
from django.test import SimpleTestCase
from django.test.utils import captured_stdout, captured_stderr

class ManagementUtilityProgramNameTests(SimpleTestCase):

    def test_execute_from_command_line_with_empty_argv0_shows_empty_prog_in_help(self):
        argv = ['', 'help']
        with captured_stdout() as out, captured_stderr() as err:
            execute_from_command_line(argv)
        self.assertIn("Type ' help <subcommand>'", out.getvalue())
        self.assertEqual(err.getvalue(), '')

    def test_management_utility_main_help_text_with_empty_argv0(self):
        mu = ManagementUtility(['', 'help'])
        text = mu.main_help_text()
        self.assertIn("Type ' help <subcommand>'", text)

    def test_management_utility_execute_with_empty_argv0_prints_help(self):
        mu = ManagementUtility(['', 'help'])
        with captured_stdout() as out, captured_stderr() as err:
            mu.execute()
        self.assertIn("Type ' help <subcommand>'", out.getvalue())
        self.assertEqual(err.getvalue(), '')

    def test_execute_from_command_line_uses_provided_argv_not_sys_argv_when_empty_prog(self):
        argv = ['', 'help']
        with mock.patch('sys.argv', ['some-other-program', 'help']):
            with captured_stdout() as out, captured_stderr() as err:
                execute_from_command_line(argv)
        self.assertIn("Type ' help <subcommand>'", out.getvalue())

import unittest
from django.core.management import ManagementUtility, execute_from_command_line
from django.test.utils import captured_stdout, captured_stderr

class ManagementUtilityArgvEdgeCasesTests(unittest.TestCase):

    def test_init_argv0_none_raises_typeerror(self):
        with self.assertRaises(TypeError):
            ManagementUtility([None, 'help'])

    def test_execute_from_command_line_argv0_none_raises_typeerror(self):
        with self.assertRaises(TypeError):
            execute_from_command_line([None, 'help'])

    def test_init_argv0_zero_raises_typeerror(self):
        with self.assertRaises(TypeError):
            ManagementUtility([0, 'help'])

    def test_execute_from_command_line_argv0_zero_raises_typeerror(self):
        with self.assertRaises(TypeError):
            execute_from_command_line([0, 'help'])

    def test_init_argv0_false_raises_typeerror(self):
        with self.assertRaises(TypeError):
            ManagementUtility([False, 'help'])

    def test_execute_from_command_line_argv0_false_raises_typeerror(self):
        with self.assertRaises(TypeError):
            execute_from_command_line([False, 'help'])

    def test_execute_help_subcommand_empty_prog_usage(self):
        with captured_stdout() as out, captured_stderr():
            execute_from_command_line(['', 'help', 'shell'])
        self.assertIn('usage:  shell', out.getvalue())

    def test_program_name_from_argv_unaffected(self):
        args = ['help', 'shell']
        with captured_stdout() as out, captured_stderr() as err:
            execute_from_command_line(['django-admin'] + args)
        self.assertIn('usage: django-admin shell', out.getvalue())
        self.assertEqual(err.getvalue(), '')

from io import StringIO
import sys
import os
from django.core.management import ManagementUtility, execute_from_command_line
from django.test import SimpleTestCase
from django.test.utils import captured_stdout, captured_stderr
from django import get_version

class ManagementUtilityProgNameTests(SimpleTestCase):

    def test_argv0_none_raises_typeerror(self):
        with self.assertRaises(TypeError):
            ManagementUtility(argv=[None, 'help'])

    def test_argv0_zero_raises_typeerror(self):
        with self.assertRaises(TypeError):
            ManagementUtility(argv=[0, 'help'])

    def test_argv0_false_raises_typeerror(self):
        with self.assertRaises(TypeError):
            ManagementUtility(argv=[False, 'help'])

    def test_empty_string_sets_empty_prog_name(self):
        util = ManagementUtility(argv=['', 'help'])
        self.assertEqual(util.prog_name, '')

    def test_execute_from_command_line_with_none_argv0_raises_typeerror(self):
        with self.assertRaises(TypeError):
            execute_from_command_line([None, 'help'])

    def test_program_name_retained_for_paths_with_extension(self):
        util = ManagementUtility(argv=[os.path.join('/opt', 'django-admin.py'), 'help'])
        self.assertEqual(util.prog_name, 'django-admin.py')

import io
import contextlib
from django.core.management import ManagementUtility, execute_from_command_line
from django.test import SimpleTestCase
import io
import contextlib
from django.core.management import ManagementUtility, execute_from_command_line
from django.test import SimpleTestCase

class ManagementUtilityEdgeCases(SimpleTestCase):

    def test_init_with_argv0_none_raises_typeerror(self):
        with self.assertRaises(TypeError):
            ManagementUtility([None, 'help'])

    def test_init_with_argv0_zero_raises_typeerror(self):
        with self.assertRaises(TypeError):
            ManagementUtility([0, 'help'])

    def test_init_with_argv0_false_raises_typeerror(self):
        with self.assertRaises(TypeError):
            ManagementUtility([False, 'help'])

    def test_prog_name_is_empty_string_when_argv0_is_empty_string(self):
        m = ManagementUtility(['', 'help'])
        self.assertEqual(m.prog_name, '')

    def test_execute_from_command_line_with_argv0_none_raises_typeerror(self):
        with self.assertRaises(TypeError):
            execute_from_command_line([None, 'help'])

    def test_execute_from_command_line_with_argv0_zero_raises_typeerror(self):
        with self.assertRaises(TypeError):
            execute_from_command_line([0, 'help'])

# No additional imports required.
from django.test import SimpleTestCase
from django.core.management import ManagementUtility, execute_from_command_line

class ManagementUtilityArgvValidationTests(SimpleTestCase):
    def test_init_raises_with_none_first_element(self):
        with self.assertRaises(TypeError):
            ManagementUtility([None, 'help'])

    def test_execute_from_command_line_raises_with_none_first_element(self):
        with self.assertRaises(TypeError):
            execute_from_command_line([None, 'help'])

    def test_init_raises_with_zero_first_element(self):
        with self.assertRaises(TypeError):
            ManagementUtility([0, 'help'])

    def test_execute_from_command_line_raises_with_zero_first_element(self):
        with self.assertRaises(TypeError):
            execute_from_command_line([0, 'help'])

    def test_init_raises_with_false_first_element(self):
        with self.assertRaises(TypeError):
            ManagementUtility([False, 'help'])

    def test_execute_from_command_line_raises_with_false_first_element(self):
        with self.assertRaises(TypeError):
            execute_from_command_line([False, 'help'])

    def test_init_raises_with_empty_list_first_element(self):
        with self.assertRaises(TypeError):
            ManagementUtility([[], 'help'])

    def test_execute_from_command_line_raises_with_empty_list_first_element(self):
        with self.assertRaises(TypeError):
            execute_from_command_line([[], 'help'])

    def test_init_raises_with_single_zero_element(self):
        with self.assertRaises(TypeError):
            ManagementUtility([0])

    def test_execute_from_command_line_raises_with_single_false_element(self):
        with self.assertRaises(TypeError):
            execute_from_command_line([False])

from django.test import SimpleTestCase
from django.core.management import execute_from_command_line
from django.test.utils import captured_stdout, captured_stderr

class ManagementUtilityArgvValidation(SimpleTestCase):

    def test_init_argv0_none_raises_typeerror(self):
        from django.core.management import ManagementUtility
        with self.assertRaises(TypeError):
            ManagementUtility(argv=[None, 'help'])

    def test_execute_from_command_line_argv0_none_raises_typeerror(self):
        with self.assertRaises(TypeError):
            execute_from_command_line([None, 'help'])

    def test_init_argv0_zero_raises_typeerror(self):
        from django.core.management import ManagementUtility
        with self.assertRaises(TypeError):
            ManagementUtility(argv=[0, 'help'])

    def test_execute_from_command_line_argv0_zero_raises_typeerror(self):
        with self.assertRaises(TypeError):
            execute_from_command_line([0, 'help'])

    def test_init_empty_string_uses_empty_progname(self):
        from django.core.management import ManagementUtility
        mu = ManagementUtility(argv=['', 'help'])
        self.assertEqual(mu.prog_name, '')

    def test_managementutility_execute_help_emits_main_help_text(self):
        from django.core.management import ManagementUtility
        mu = ManagementUtility(argv=['/bin/django', 'help'])
        with captured_stdout() as out, captured_stderr() as err:
            mu.execute()
        self.assertIn("Type 'django help <subcommand>'", out.getvalue())

from django.test import SimpleTestCase
from django.test.utils import captured_stdout
from django.core.management import ManagementUtility, execute_from_command_line
import sys

class ManagementUtilityProgNameEdgeCasesTests(SimpleTestCase):

    def test_init_raises_typeerror_when_argv0_is_none(self):
        with self.assertRaises(TypeError):
            ManagementUtility([None, 'help'])

    def test_execute_from_command_line_raises_typeerror_when_argv0_is_none(self):
        with self.assertRaises(TypeError):
            execute_from_command_line([None, 'help'])

    def test_prog_name_is_empty_string_when_argv0_is_empty(self):
        mu = ManagementUtility(['', 'help'])
        self.assertEqual(mu.prog_name, '')

from django.core.management import ManagementUtility, execute_from_command_line
from django.test import SimpleTestCase
from django.test.utils import captured_stdout
import sys

class ProgramNameRegressionTests(SimpleTestCase):

    def test_init_with_none_argv0_raises_type_error(self):
        """
        ManagementUtility should raise a TypeError when argv[0] is None,
        matching the original behavior where os.path.basename(None) raises.
        The candidate patch avoided the exception; this test would FAIL under it.
        """
        with self.assertRaises(TypeError):
            ManagementUtility(argv=[None, 'help'])

    def test_execute_from_command_line_with_none_argv0_raises_type_error(self):
        """
        execute_from_command_line() should raise a TypeError when its argv[0] is None.
        """
        with self.assertRaises(TypeError):
            execute_from_command_line([None, 'help'])

    def test_management_utility_execute_with_none_argv0_raises_type_error(self):
        """
        Instantiating and executing ManagementUtility with argv[0] == None should
        raise during initialization (TypeError).
        """
        with self.assertRaises(TypeError):
            mu = ManagementUtility(argv=[None, 'help'])
            mu.execute()

    def test_prog_name_is_empty_string_when_argv0_is_empty_string(self):
        """
        When argv[0] is an empty string, ManagementUtility.prog_name should be
        os.path.basename('') == '' (gold behavior). The candidate patch would
        replace it with 'django-admin'.
        """
        mu = ManagementUtility(argv=['', 'help'])
        self.assertEqual(mu.prog_name, '')