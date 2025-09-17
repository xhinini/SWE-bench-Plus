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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 auth_tests.test_auth_backends_llm.AuthenticateShortCircuitTests.setUp auth_tests.test_auth_backends_llm.AuthenticateShortCircuitTests.test_empty_credentials_dict_short_circuits auth_tests.test_auth_backends_llm.AuthenticateShortCircuitTests.test_explicit_none_password_for_customuser_with_email_username_field auth_tests.test_auth_backends_llm.AuthenticateShortCircuitTests.test_missing_password_for_user_model_without_is_active_field auth_tests.test_auth_backends_llm.AuthenticateShortCircuitTests.test_no_password_for_custompermissions_user auth_tests.test_auth_backends_llm.AuthenticateShortCircuitTests.test_no_password_for_customuser_with_email_username_field auth_tests.test_auth_backends_llm.AuthenticateShortCircuitTests.test_no_password_for_extension_user auth_tests.test_auth_backends_llm.AuthenticateShortCircuitTests.test_no_password_for_uuid_user auth_tests.test_auth_backends_llm.AuthenticateShortCircuitTests.test_password_only_short_circuits auth_tests.test_auth_backends_llm.AuthenticateShortCircuitTests.test_unrelated_kwarg_and_no_password_short_circuits auth_tests.test_auth_backends_llm.AuthenticateShortCircuitTests.test_username_none_and_password_present_short_circuits
coverage json -o coverage.json
: '>>>>> End Test Output'
