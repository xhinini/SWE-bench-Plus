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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 auth_tests.test_auth_backends_llm.ModelBackendAuthenticateRegressionTests.setUp auth_tests.test_auth_backends_llm.ModelBackendAuthenticateRegressionTests.test_authenticate_returns_none_not_false_when_no_credentials auth_tests.test_auth_backends_llm.ModelBackendAuthenticateRegressionTests.test_authenticate_with_usernamefield_and_password_returns_user auth_tests.test_auth_backends_llm.ModelBackendAuthenticateRegressionTests.test_empty_string_username_calls_get_by_natural_key auth_tests.test_auth_backends_llm.ModelBackendAuthenticateRegressionTests.test_no_credentials_no_lookup_no_set_password auth_tests.test_auth_backends_llm.ModelBackendAuthenticateRegressionTests.test_no_db_queries_when_only_password_provided auth_tests.test_auth_backends_llm.ModelBackendAuthenticateRegressionTests.test_no_db_queries_when_only_username_provided auth_tests.test_auth_backends_llm.ModelBackendAuthenticateRegressionTests.test_password_provided_but_no_username_no_lookup auth_tests.test_auth_backends_llm.ModelBackendAuthenticateRegressionTests.test_username_in_kwargs_but_no_password_no_lookup
coverage json -o coverage.json
: '>>>>> End Test Output'
