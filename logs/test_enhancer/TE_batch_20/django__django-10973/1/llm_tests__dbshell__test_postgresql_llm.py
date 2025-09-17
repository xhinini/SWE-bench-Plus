import os
import subprocess
from unittest import mock
from django.db.backends.postgresql.client import DatabaseClient
from django.test import SimpleTestCase

class PostgreSqlDbshellAdditionalTests(SimpleTestCase):

    def test_password_as_int(self):
        args, pwd = self._run_it({'database': 'dbname', 'user': 'u', 'password': 1234})
        self.assertEqual(args, ['psql', '-U', 'u', 'dbname'])
        self.assertEqual(pwd, str(1234))

    def test_password_as_bytes(self):
        pw = b'secret'
        args, pwd = self._run_it({'database': 'dbname', 'user': 'u', 'password': pw})
        self.assertEqual(args, ['psql', '-U', 'u', 'dbname'])
        self.assertEqual(pwd, str(pw))

    def test_password_as_bool_true(self):
        args, pwd = self._run_it({'database': 'dbname', 'user': 'u', 'password': True})
        self.assertEqual(args, ['psql', '-U', 'u', 'dbname'])
        self.assertEqual(pwd, str(True))

    def test_password_as_float(self):
        pw = 12.34
        args, pwd = self._run_it({'database': 'dbname', 'user': 'u', 'password': pw})
        self.assertEqual(args, ['psql', '-U', 'u', 'dbname'])
        self.assertEqual(pwd, str(pw))

    def test_password_as_bytearray(self):
        pw = bytearray(b'pw')
        args, pwd = self._run_it({'database': 'dbname', 'user': 'u', 'password': pw})
        self.assertEqual(args, ['psql', '-U', 'u', 'dbname'])
        self.assertEqual(pwd, str(pw))

    def test_password_as_list(self):
        pw = ['a', 'b']
        args, pwd = self._run_it({'database': 'dbname', 'user': 'u', 'password': pw})
        self.assertEqual(args, ['psql', '-U', 'u', 'dbname'])
        self.assertEqual(pwd, str(pw))

    def test_password_custom_object_with_str(self):

        class P:

            def __str__(self):
                return 'custompw'
        pw = P()
        args, pwd = self._run_it({'database': 'dbname', 'user': 'u', 'password': pw})
        self.assertEqual(args, ['psql', '-U', 'u', 'dbname'])
        self.assertEqual(pwd, str(pw))

    def test_password_bytes_with_non_ascii(self):
        pw = b'\xc3\xa9'
        args, pwd = self._run_it({'database': 'dbname', 'user': 'u', 'password': pw})
        self.assertEqual(args, ['psql', '-U', 'u', 'dbname'])
        self.assertEqual(pwd, str(pw))

    def test_password_object_returning_unicode(self):

        class P:

            def __str__(self):
                return 'sésame'
        pw = P()
        args, pwd = self._run_it({'database': 'dbname', 'user': 'u', 'password': pw})
        self.assertEqual(args, ['psql', '-U', 'u', 'dbname'])
        self.assertEqual(pwd, str(pw))

    def test_password_large_complex_object(self):

        class ComplexPW:

            def __repr__(self):
                return '<ComplexPW>'

            def __str__(self):
                return 'complex:pw:with:colons'
        pw = ComplexPW()
        args, pwd = self._run_it({'database': 'dbname', 'user': 'u', 'password': pw})
        self.assertEqual(args, ['psql', '-U', 'u', 'dbname'])
        self.assertEqual(pwd, str(pw))

import os
import signal
import subprocess
from unittest import mock
from django.db.backends.postgresql.client import DatabaseClient
from django.test import SimpleTestCase

class PostgreSqlDbshellCommandTestCase(SimpleTestCase):

    def test_password_int_conversion(self):
        args, pgpassword = self._run_it({'database': 'dbname', 'user': 'u', 'password': 12345, 'host': 'h', 'port': '444'})
        self.assertEqual(pgpassword, '12345')
        self.assertIn('-p', args)
        self.assertIn('444', args)

    def test_password_bytes_conversion(self):
        args, pgpassword = self._run_it({'database': 'dbname', 'user': 'u', 'password': b'bytepw', 'host': 'h', 'port': '444'})
        self.assertEqual(pgpassword, "b'bytepw'")

    def test_password_object_conversion(self):

        class P:

            def __str__(self):
                return 'objpw'
        args, pgpassword = self._run_it({'database': 'dbname', 'user': 'u', 'password': P(), 'host': 'h', 'port': '444'})
        self.assertEqual(pgpassword, 'objpw')

    def test_password_bool_conversion(self):
        args, pgpassword = self._run_it({'database': 'dbname', 'user': 'u', 'password': True, 'host': 'h', 'port': '444'})
        self.assertEqual(pgpassword, 'True')

    def test_subprocess_run_called_with_check_true_and_string_env(self):
        with mock.patch('subprocess.run') as mock_run:
            mock_run.return_value = subprocess.CompletedProcess([], 0)
            DatabaseClient.runshell_db({'database': 'dbname', 'user': 'u', 'password': 9876, 'host': 'h', 'port': 444})
            self.assertTrue(mock_run.called)
            _, call_kwargs = mock_run.call_args
            self.assertIn('check', call_kwargs)
            self.assertTrue(call_kwargs['check'])
            self.assertIn('env', call_kwargs)
            self.assertIsInstance(call_kwargs['env'].get('PGPASSWORD'), str)
            self.assertEqual(call_kwargs['env'].get('PGPASSWORD'), '9876')