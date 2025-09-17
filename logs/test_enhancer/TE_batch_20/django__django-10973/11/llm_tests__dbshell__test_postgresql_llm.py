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

import os
import signal
import subprocess
from unittest import mock
from django.db.backends.postgresql.client import DatabaseClient
from django.test import SimpleTestCase

class PostgreSqlDbshellCommandTestCase(SimpleTestCase):

    def test_password_bytes_converted_to_str(self):
        args, pgpassword = self._run_it({'database': 'dbname', 'password': b'secret-bytes'})
        self.assertEqual(args, ['psql', 'dbname'])
        self.assertEqual(pgpassword, str(b'secret-bytes'))

    def test_password_int_converted_to_str(self):
        args, pgpassword = self._run_it({'database': 'dbname', 'password': 12345})
        self.assertEqual(args, ['psql', 'dbname'])
        self.assertEqual(pgpassword, '12345')

    def test_password_object_converted_to_str(self):

        class P:

            def __str__(self):
                return 'obj-pass'
        p = P()
        args, pgpassword = self._run_it({'database': 'dbname', 'password': p})
        self.assertEqual(args, ['psql', 'dbname'])
        self.assertEqual(pgpassword, 'obj-pass')

    def test_password_bytes_with_colon_converted_to_str(self):
        pwd = b'some:colon'
        args, pgpassword = self._run_it({'database': 'dbname', 'password': pwd})
        self.assertEqual(args, ['psql', 'dbname'])
        self.assertEqual(pgpassword, str(pwd))

    def test_password_bool_converted_to_str(self):
        args, pgpassword = self._run_it({'database': 'dbname', 'password': True})
        self.assertEqual(args, ['psql', 'dbname'])
        self.assertEqual(pgpassword, 'True')

from unittest import mock
import os
import subprocess
from unittest import mock
from django.db.backends.postgresql.client import DatabaseClient
from django.test import SimpleTestCase

class AdditionalPostgreSqlDbshellTests(SimpleTestCase):

    def test_password_bytes(self):
        args, pgpw = self._run_it({'database': 'dbname', 'user': 'u', 'password': b'secret-bytes', 'host': 'h', 'port': '1'})
        self.assertEqual(pgpw, str(b'secret-bytes'))
        self.assertIn('dbname', args)

    def test_password_int(self):
        args, pgpw = self._run_it({'database': 'dbname', 'user': 'u', 'password': 12345, 'host': 'h', 'port': '1'})
        self.assertEqual(pgpw, str(12345))

    def test_password_bool_true(self):
        args, pgpw = self._run_it({'database': 'dbname', 'user': 'u', 'password': True, 'host': 'h', 'port': '1'})
        self.assertEqual(pgpw, str(True))

    def test_password_custom_object_with_str(self):

        class PwdObj:

            def __str__(self):
                return 'obj-pass'
        pwd = PwdObj()
        args, pgpw = self._run_it({'database': 'dbname', 'user': 'u', 'password': pwd, 'host': 'h', 'port': '1'})
        self.assertEqual(pgpw, str(pwd))

    def test_password_bytearray(self):
        ba = bytearray(b'byte-array')
        args, pgpw = self._run_it({'database': 'dbname', 'user': 'u', 'password': ba, 'host': 'h', 'port': '1'})
        self.assertEqual(pgpw, str(ba))

    def test_password_non_ascii_bytes(self):
        non_ascii = b'\xc3\xa9'
        args, pgpw = self._run_it({'database': 'dbname', 'user': 'u', 'password': non_ascii, 'host': 'h', 'port': '1'})
        self.assertEqual(pgpw, str(non_ascii))

from decimal import Decimal
from fractions import Fraction
import os
import signal
import subprocess
from unittest import mock
from decimal import Decimal
from fractions import Fraction
from django.db.backends.postgresql.client import DatabaseClient
from django.test import SimpleTestCase

class PostgreSqlDbshellCommandTestCase(SimpleTestCase):

    def test_password_int(self):
        _, pgpassword = self._run_it({'database': 'dbname', 'user': 'someuser', 'password': 123, 'host': 'somehost', 'port': '444'})
        self.assertEqual(pgpassword, '123')

    def test_password_float(self):
        _, pgpassword = self._run_it({'database': 'dbname', 'user': 'someuser', 'password': 3.14, 'host': 'somehost', 'port': '444'})
        self.assertEqual(pgpassword, '3.14')

    def test_password_bool_true(self):
        _, pgpassword = self._run_it({'database': 'dbname', 'user': 'someuser', 'password': True, 'host': 'somehost', 'port': '444'})
        self.assertEqual(pgpassword, 'True')

    def test_password_bytes(self):
        pwd = b'secret'
        _, pgpassword = self._run_it({'database': 'dbname', 'user': 'someuser', 'password': pwd, 'host': 'somehost', 'port': '444'})
        self.assertEqual(pgpassword, str(pwd))

    def test_password_bytearray(self):
        pwd = bytearray(b'abc')
        _, pgpassword = self._run_it({'database': 'dbname', 'user': 'someuser', 'password': pwd, 'host': 'somehost', 'port': '444'})
        self.assertEqual(pgpassword, str(pwd))

    def test_password_decimal(self):
        pwd = Decimal('1.23')
        _, pgpassword = self._run_it({'database': 'dbname', 'user': 'someuser', 'password': pwd, 'host': 'somehost', 'port': '444'})
        self.assertEqual(pgpassword, str(pwd))

    def test_password_fraction(self):
        pwd = Fraction(2, 3)
        _, pgpassword = self._run_it({'database': 'dbname', 'user': 'someuser', 'password': pwd, 'host': 'somehost', 'port': '444'})
        self.assertEqual(pgpassword, str(pwd))

    def test_password_custom_object(self):

        class P:

            def __str__(self):
                return 'custom-pass'
        pwd = P()
        _, pgpassword = self._run_it({'database': 'dbname', 'user': 'someuser', 'password': pwd, 'host': 'somehost', 'port': '444'})
        self.assertEqual(pgpassword, 'custom-pass')

    def test_password_custom_unicode_object(self):

        class P:

            def __str__(self):
                return 'sésame'
        pwd = P()
        _, pgpassword = self._run_it({'database': 'dbname', 'user': 'someuser', 'password': pwd, 'host': 'somehost', 'port': '444'})
        self.assertEqual(pgpassword, 'sésame')

import os
import signal
import subprocess
from unittest import mock
from django.db.backends.postgresql.client import DatabaseClient
from django.test import SimpleTestCase

class PostgreSqlDbshellCommandTestCase(SimpleTestCase):

    def test_password_bytes(self):
        passwd = b'secret-bytes'
        args, env = self._run_and_capture_env({'database': 'dbname', 'password': passwd})
        self.assertEqual(env.get('PGPASSWORD'), str(passwd))

    def test_password_int(self):
        passwd = 4242
        args, env = self._run_and_capture_env({'database': 'dbname', 'password': passwd})
        self.assertEqual(env.get('PGPASSWORD'), str(passwd))

    def test_password_float(self):
        passwd = 3.14159
        args, env = self._run_and_capture_env({'database': 'dbname', 'password': passwd})
        self.assertEqual(env.get('PGPASSWORD'), str(passwd))

    def test_password_complex(self):
        passwd = 1 + 2j
        args, env = self._run_and_capture_env({'database': 'dbname', 'password': passwd})
        self.assertEqual(env.get('PGPASSWORD'), str(passwd))

    def test_password_tuple(self):
        passwd = ('a', 'b')
        args, env = self._run_and_capture_env({'database': 'dbname', 'password': passwd})
        self.assertEqual(env.get('PGPASSWORD'), str(passwd))

    def test_password_list(self):
        passwd = [1, 2, 3]
        args, env = self._run_and_capture_env({'database': 'dbname', 'password': passwd})
        self.assertEqual(env.get('PGPASSWORD'), str(passwd))

    def test_password_dict(self):
        passwd = {'k': 'v'}
        args, env = self._run_and_capture_env({'database': 'dbname', 'password': passwd})
        self.assertEqual(env.get('PGPASSWORD'), str(passwd))

    def test_password_set(self):
        passwd = {'x', 'y'}
        args, env = self._run_and_capture_env({'database': 'dbname', 'password': passwd})
        self.assertEqual(env.get('PGPASSWORD'), str(passwd))

    def test_password_bool_true(self):
        passwd = True
        args, env = self._run_and_capture_env({'database': 'dbname', 'password': passwd})
        self.assertEqual(env.get('PGPASSWORD'), str(passwd))

    def test_password_custom_object(self):

        class Token:

            def __str__(self):
                return 'tokén-✓'
        passwd = Token()
        args, env = self._run_and_capture_env({'database': 'dbname', 'password': passwd})
        self.assertEqual(env.get('PGPASSWORD'), str(passwd))

import os
import subprocess
from unittest import mock
import os
import subprocess
from unittest import mock
from django.db.backends.postgresql.client import DatabaseClient
from django.test import SimpleTestCase

class PostgreSqlDbshellAdditionalTests(SimpleTestCase):

    def test_password_bytes_converted_to_str(self):
        pwd = b'secret-bytes'
        _, pg = self._run_and_get_pgpassword({'database': 'dbname', 'user': 'user', 'password': pwd})
        self.assertEqual(pg, str(pwd))
        self.assertIsInstance(pg, str)

    def test_password_bytearray_converted_to_str(self):
        pwd = bytearray(b'secret-bytearray')
        _, pg = self._run_and_get_pgpassword({'database': 'dbname', 'user': 'user', 'password': pwd})
        self.assertEqual(pg, str(pwd))
        self.assertIsInstance(pg, str)

    def test_password_int_converted_to_str(self):
        pwd = 123456
        _, pg = self._run_and_get_pgpassword({'database': 'dbname', 'user': 'user', 'password': pwd})
        self.assertEqual(pg, str(pwd))
        self.assertIsInstance(pg, str)

    def test_password_float_converted_to_str(self):
        pwd = 3.14159
        _, pg = self._run_and_get_pgpassword({'database': 'dbname', 'user': 'user', 'password': pwd})
        self.assertEqual(pg, str(pwd))
        self.assertIsInstance(pg, str)

    def test_password_bool_converted_to_str(self):
        pwd = True
        _, pg = self._run_and_get_pgpassword({'database': 'dbname', 'user': 'user', 'password': pwd})
        self.assertEqual(pg, str(pwd))
        self.assertIsInstance(pg, str)

    def test_password_list_converted_to_str(self):
        pwd = ['a', 'b', 1]
        _, pg = self._run_and_get_pgpassword({'database': 'dbname', 'user': 'user', 'password': pwd})
        self.assertEqual(pg, str(pwd))
        self.assertIsInstance(pg, str)

    def test_password_tuple_converted_to_str(self):
        pwd = ('x', 2)
        _, pg = self._run_and_get_pgpassword({'database': 'dbname', 'user': 'user', 'password': pwd})
        self.assertEqual(pg, str(pwd))
        self.assertIsInstance(pg, str)

    def test_password_single_item_dict_converted_to_str(self):
        pwd = {'k': 'v'}
        _, pg = self._run_and_get_pgpassword({'database': 'dbname', 'user': 'user', 'password': pwd})
        self.assertEqual(pg, str(pwd))
        self.assertIsInstance(pg, str)

    def test_password_single_item_set_converted_to_str(self):
        pwd = {1}
        _, pg = self._run_and_get_pgpassword({'database': 'dbname', 'user': 'user', 'password': pwd})
        self.assertEqual(pg, str(pwd))
        self.assertIsInstance(pg, str)

    def test_password_custom_object_converted_to_str(self):

        class P:

            def __str__(self):
                return 'custom-object-password'
        pwd = P()
        _, pg = self._run_and_get_pgpassword({'database': 'dbname', 'user': 'user', 'password': pwd})
        self.assertEqual(pg, str(pwd))
        self.assertIsInstance(pg, str)

import os
import subprocess
from unittest import mock
from django.db.backends.postgresql.client import DatabaseClient
from django.test import SimpleTestCase

class PostgreSqlDbshellPasswordTypeTests(SimpleTestCase):

    def test_password_int(self):
        password = 12345
        _, pgpassword = self._run_it({'database': 'dbname', 'user': 'user', 'password': password})
        self.assertEqual(pgpassword, str(password))

    def test_password_bytes(self):
        password = b'secret'
        _, pgpassword = self._run_it({'database': 'dbname', 'user': 'user', 'password': password})
        self.assertEqual(pgpassword, str(password))

    def test_password_custom_object(self):

        class P:

            def __str__(self):
                return 'custom-pw'
        password = P()
        _, pgpassword = self._run_it({'database': 'dbname', 'user': 'user', 'password': password})
        self.assertEqual(pgpassword, str(password))

    def test_password_bool_true(self):
        password = True
        _, pgpassword = self._run_it({'database': 'dbname', 'user': 'user', 'password': password})
        self.assertEqual(pgpassword, str(password))

    def test_password_list(self):
        password = [1, 2, 3]
        _, pgpassword = self._run_it({'database': 'dbname', 'user': 'user', 'password': password})
        self.assertEqual(pgpassword, str(password))

    def test_password_tuple(self):
        password = (1, 2)
        _, pgpassword = self._run_it({'database': 'dbname', 'user': 'user', 'password': password})
        self.assertEqual(pgpassword, str(password))

    def test_password_float(self):
        password = 3.14159
        _, pgpassword = self._run_it({'database': 'dbname', 'user': 'user', 'password': password})
        self.assertEqual(pgpassword, str(password))

    def test_password_set(self):
        password = {1}
        _, pgpassword = self._run_it({'database': 'dbname', 'user': 'user', 'password': password})
        self.assertEqual(pgpassword, str(password))

    def test_password_frozenset(self):
        password = frozenset({1})
        _, pgpassword = self._run_it({'database': 'dbname', 'user': 'user', 'password': password})
        self.assertEqual(pgpassword, str(password))

    def test_password_complex(self):
        password = 1 + 2j
        _, pgpassword = self._run_it({'database': 'dbname', 'user': 'user', 'password': password})
        self.assertEqual(pgpassword, str(password))

import os
import signal
import subprocess
from unittest import mock
from django.db.backends.postgresql.client import DatabaseClient
from django.test import SimpleTestCase

class PostgreSqlDbshellCommandTestCase(SimpleTestCase):

    def test_password_int_is_converted_to_str_in_env(self):
        args, env = self._capture_run_env({'database': 'd', 'user': 'u', 'password': 123})
        self.assertIn('PGPASSWORD', env)
        self.assertEqual(env['PGPASSWORD'], str(123))
        self.assertEqual(args, ['psql', '-U', 'u', 'd'])

    def test_password_bytes_is_converted_to_str_in_env(self):
        pw = b'bytespass'
        args, env = self._capture_run_env({'database': 'd2', 'user': 'u2', 'password': pw})
        self.assertIn('PGPASSWORD', env)
        self.assertEqual(env['PGPASSWORD'], str(pw))
        self.assertEqual(args, ['psql', '-U', 'u2', 'd2'])

    def test_password_bool_is_converted_to_str_in_env(self):
        pw = True
        args, env = self._capture_run_env({'database': 'd3', 'user': 'u3', 'password': pw})
        self.assertIn('PGPASSWORD', env)
        self.assertEqual(env['PGPASSWORD'], str(pw))
        self.assertEqual(args, ['psql', '-U', 'u3', 'd3'])

    def test_password_list_is_converted_to_str_in_env(self):
        pw = [1, 2, 3]
        args, env = self._capture_run_env({'database': 'd4', 'user': 'u4', 'password': pw})
        self.assertIn('PGPASSWORD', env)
        self.assertEqual(env['PGPASSWORD'], str(pw))
        self.assertEqual(args, ['psql', '-U', 'u4', 'd4'])

    def test_password_object_is_converted_to_str_in_env(self):

        class PwdObj:

            def __str__(self):
                return 'objpass'
        pw = PwdObj()
        args, env = self._capture_run_env({'database': 'd5', 'user': 'u5', 'password': pw})
        self.assertIn('PGPASSWORD', env)
        self.assertEqual(env['PGPASSWORD'], str(pw))
        self.assertEqual(args, ['psql', '-U', 'u5', 'd5'])

import os
import signal
import subprocess
from unittest import mock
from django.db.backends.postgresql.client import DatabaseClient
from django.test import SimpleTestCase

class PostgreSqlDbshellCommandTestCase(SimpleTestCase):

    def test_password_int_is_stringified(self):
        password = 12345
        args, pgpassword = self._run_it({'database': 'dbname', 'password': password})
        self.assertEqual(pgpassword, str(password))
        self.assertEqual(args[-1], 'dbname')

    def test_password_float_is_stringified(self):
        password = 3.14159
        args, pgpassword = self._run_it({'database': 'dbname', 'password': password})
        self.assertEqual(pgpassword, str(password))

    def test_password_complex_is_stringified(self):
        password = 1 + 2j
        args, pgpassword = self._run_it({'database': 'dbname', 'password': password})
        self.assertEqual(pgpassword, str(password))

    def test_password_bytes_is_stringified(self):
        password = b'secret-bytes'
        args, pgpassword = self._run_it({'database': 'dbname', 'password': password})
        self.assertEqual(pgpassword, str(password))

    def test_password_bytearray_is_stringified(self):
        password = bytearray(b'pw')
        args, pgpassword = self._run_it({'database': 'dbname', 'password': password})
        self.assertEqual(pgpassword, str(password))

    def test_password_list_is_stringified(self):
        password = [1, 2, 3]
        args, pgpassword = self._run_it({'database': 'dbname', 'password': password})
        self.assertEqual(pgpassword, str(password))

    def test_password_tuple_is_stringified(self):
        password = (1, 2)
        args, pgpassword = self._run_it({'database': 'dbname', 'password': password})
        self.assertEqual(pgpassword, str(password))

    def test_password_custom_object_is_stringified(self):

        class Secret:

            def __str__(self):
                return 'mysecret'
        password = Secret()
        args, pgpassword = self._run_it({'database': 'dbname', 'password': password})
        self.assertEqual(pgpassword, 'mysecret')

    def test_password_custom_unicode_object_is_stringified(self):

        class SecretU:

            def __str__(self):
                return 'sésame'
        password = SecretU()
        args, pgpassword = self._run_it({'database': 'dbname', 'password': password})
        self.assertEqual(pgpassword, 'sésame')

    def test_password_bytearray_and_other_non_string_types_truthy(self):
        password = bytearray(b'xyz')
        args, pgpassword = self._run_it({'database': 'dbname', 'password': password})
        self.assertEqual(pgpassword, str(password))