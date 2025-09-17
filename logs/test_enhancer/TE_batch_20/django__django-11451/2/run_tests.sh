#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
sed -i '/en_US.UTF-8/s/^# //g' /etc/locale.gen && locale-gen
export LANG=en_US.UTF-8
export LANGUAGE=en_US:en
export LC_ALL=en_US.UTF-8
export PYTHONIOENCODING=utf8
python --version && python -m pip install -U pip
python -m pip install -U 'coverage==6.2'

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 auth_tests.test_auth_backends_llm.CountingMD5PasswordHasher.encode auth_tests.test_auth_backends_llm.ModelBackendAuthenticatePasswordNoneTests.setUpTestData auth_tests.test_auth_backends_llm.ModelBackendAuthenticatePasswordNoneTests.test_backend_authenticate_with_kwargs_username_field_and_password_none_no_db auth_tests.test_auth_backends_llm.ModelBackendAuthenticatePasswordNoneTests.test_empty_string_password_triggers_normal_lookup_and_hash auth_tests.test_auth_backends_llm.ModelBackendAuthenticatePasswordNoneTests.test_get_by_natural_key_not_called_when_username_provided_but_password_none_via_kwargs
coverage json -o coverage.json
: '>>>>> End Test Output'
