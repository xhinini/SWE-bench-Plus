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