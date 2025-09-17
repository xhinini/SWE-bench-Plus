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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 auth_tests.test_auth_backends_llm.ModelBackendAuthenticateMissingCredentialsTests.setUpTestData auth_tests.test_auth_backends_llm.ModelBackendAuthenticateMissingCredentialsTests.test_direct_backend_called_with_kwargs_missing_username_value_no_db_or_hashing auth_tests.test_auth_backends_llm.ModelBackendAuthenticateMissingCredentialsTests.test_kwargs_username_field_with_password_proceeds_to_authenticate auth_tests.test_auth_backends_llm.ModelBackendAuthenticateMissingCredentialsTests.test_multiple_missing_credentials_calls_do_not_accumulate_hash_calls auth_tests.test_auth_backends_llm.ModelBackendAuthenticateMissingCredentialsTests.test_no_credentials_direct_backend_no_db_or_hashing auth_tests.test_auth_backends_llm.ModelBackendAuthenticateMissingCredentialsTests.test_top_level_authenticate_missing_credentials_no_db_or_hashing auth_tests.test_auth_backends_llm.ModelBackendAuthenticateMissingCredentialsTests.test_username_none_password_none_with_kwargs_usernamefield_no_db_or_hashing auth_tests.test_auth_backends_llm.ModelBackendAuthenticateMissingCredentialsTests.test_with_request_present_and_missing_password_no_db_or_hashing
coverage json -o coverage.json
: '>>>>> End Test Output'
