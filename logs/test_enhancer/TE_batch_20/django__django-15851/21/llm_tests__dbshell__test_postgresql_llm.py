def test_parameters_default_db_when_name_missing(self):
    args, env = self.settings_to_cmd_args_env({}, ['--help'])
    self.assertEqual(args, ['psql', '--help', 'postgres'])
    self.assertIsNone(env)

def test_parameters_with_host_port_and_default_db(self):
    settings = {'HOST': 'localhost', 'PORT': 5432}
    args, env = self.settings_to_cmd_args_env(settings, ['-c', 'SELECT 1'])
    self.assertEqual(args, ['psql', '-h', 'localhost', '-p', '5432', '-c', 'SELECT 1', 'postgres'])
    self.assertIsNone(env)

def test_parameters_default_db_with_empty_name(self):
    settings = {'NAME': '', 'USER': 'u'}
    args, env = self.settings_to_cmd_args_env(settings, ['--version'])
    self.assertEqual(args, ['psql', '-U', 'u', '--version', 'postgres'])
    self.assertIsNone(env)

def test_parameters_default_db_with_none_name(self):
    settings = {'NAME': None}
    args, env = self.settings_to_cmd_args_env(settings, ['--help'])
    self.assertEqual(args, ['psql', '--help', 'postgres'])
    self.assertIsNone(env)

def test_parameters_with_service_and_parameters(self):
    settings = {'OPTIONS': {'service': 'django_test'}}
    args, env = self.settings_to_cmd_args_env(settings, ['--help'])
    self.assertEqual(args, ['psql', '--help'])
    self.assertEqual(env, {'PGSERVICE': 'django_test'})

def test_parameters_with_service_and_passfile_and_parameters(self):
    settings = {'OPTIONS': {'service': 'django_test', 'passfile': '~/.pgpass'}}
    args, env = self.settings_to_cmd_args_env(settings, ['--version'])
    self.assertEqual(args, ['psql', '--version'])
    self.assertEqual(env, {'PGSERVICE': 'django_test', 'PGPASSFILE': '~/.pgpass'})

def test_user_and_parameters_with_missing_db(self):
    settings = {'USER': 'testuser'}
    args, env = self.settings_to_cmd_args_env(settings, ['--help'])
    self.assertEqual(args, ['psql', '-U', 'testuser', '--help', 'postgres'])
    self.assertIsNone(env)

def test_ipv6_host_and_parameters_with_default_db(self):
    settings = {'HOST': '::1'}
    args, env = self.settings_to_cmd_args_env(settings, ['--help'])
    self.assertEqual(args, ['psql', '-h', '::1', '--help', 'postgres'])
    self.assertIsNone(env)

def test_port_as_int_and_parameters(self):
    settings = {'PORT': 5433}
    args, env = self.settings_to_cmd_args_env(settings, ['-c', 'SELECT 42'])
    self.assertEqual(args, ['psql', '-p', '5433', '-c', 'SELECT 42', 'postgres'])
    self.assertIsNone(env)

def test_parameters_multiple_args_before_db(self):
    settings = {'HOST': 'h', 'USER': 'u'}
    params = ['-c', 'SELECT 1', '--single-transaction']
    args, env = self.settings_to_cmd_args_env(settings, params)
    self.assertEqual(args, ['psql', '-U', 'u', '-h', 'h', '-c', 'SELECT 1', '--single-transaction', 'postgres'])
    self.assertIsNone(env)

def test_parameters_before_dbname_user_host_port(self):
    settings = {'NAME': 'mydb', 'USER': 'alice', 'HOST': 'db.example', 'PORT': '5432'}
    params = ['-c', 'SELECT 1']
    args, env = self.settings_to_cmd_args_env(settings, params)
    self.assertEqual(args, ['psql', '-U', 'alice', '-h', 'db.example', '-p', '5432', '-c', 'SELECT 1', 'mydb'])
    self.assertIsNone(env)

def test_parameters_before_default_postgres_when_name_missing(self):
    settings = {}
    params = ['--version']
    args, env = self.settings_to_cmd_args_env(settings, params)
    self.assertEqual(args, ['psql', '--version', 'postgres'])
    self.assertIsNone(env)

def test_parameters_with_service_and_parameters(self):
    settings = {'OPTIONS': {'service': 'django_test'}}
    params = ['--version']
    args, env = self.settings_to_cmd_args_env(settings, params)
    self.assertEqual(args, ['psql', '--version'])
    self.assertEqual(env, {'PGSERVICE': 'django_test'})

def test_parameters_not_duplicated(self):
    settings = {'NAME': 'dupdb'}
    params = ['--help', '--help']
    args, env = self.settings_to_cmd_args_env(settings, params)
    self.assertEqual(args, ['psql', '--help', '--help', 'dupdb'])
    self.assertIsNone(env)

def test_parameters_with_dbname_like_parameter_preserves_order(self):
    settings = {'NAME': 'real_db'}
    params = ['--dbname', 'fake_db']
    args, env = self.settings_to_cmd_args_env(settings, params)
    self.assertEqual(args, ['psql', '--dbname', 'fake_db', 'real_db'])
    self.assertIsNone(env)

def test_parameters_order_with_ipv6_and_special_user(self):
    settings = {'NAME': 'somedb', 'USER': 'some:user', 'PASSWORD': 'p@ss:word', 'HOST': '::1', 'PORT': '5432'}
    params = ['-c', 'SELECT 1']
    args, env = self.settings_to_cmd_args_env(settings, params)
    self.assertEqual(args, ['psql', '-U', 'some:user', '-h', '::1', '-p', '5432', '-c', 'SELECT 1', 'somedb'])
    self.assertEqual(env, {'PGPASSWORD': 'p@ss:word'})

def test_parameters_with_passfile_and_service_and_parameters(self):
    settings = {'OPTIONS': {'service': 'svc', 'passfile': '~/.pgpass'}}
    params = ['--list']
    args, env = self.settings_to_cmd_args_env(settings, params)
    self.assertEqual(args, ['psql', '--list'])
    self.assertEqual(env, {'PGSERVICE': 'svc', 'PGPASSFILE': '~/.pgpass'})

def test_parameters_empty_list_results_in_only_dbname(self):
    settings = {'NAME': 'onlydb'}
    params = []
    args, env = self.settings_to_cmd_args_env(settings, params)
    self.assertEqual(args, ['psql', 'onlydb'])
    self.assertIsNone(env)

def test_multiple_parameter_flags_preserve_order_before_dbname(self):
    settings = {'NAME': 'scriptdb'}
    params = ['-c', 'SELECT 1', '-f', 'file.sql']
    args, env = self.settings_to_cmd_args_env(settings, params)
    self.assertEqual(args, ['psql', '-c', 'SELECT 1', '-f', 'file.sql', 'scriptdb'])
    self.assertIsNone(env)

def test_parameters_unicode_and_accent_preserved(self):
    settings = {'NAME': 'unicodedb', 'USER': 'rôle', 'PASSWORD': 'sésame'}
    params = ['--comment', 'cömment']
    args, env = self.settings_to_cmd_args_env(settings, params)
    self.assertEqual(args, ['psql', '-U', 'rôle', '--comment', 'cömment', 'unicodedb'])
    self.assertEqual(env, {'PGPASSWORD': 'sésame'})