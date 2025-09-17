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