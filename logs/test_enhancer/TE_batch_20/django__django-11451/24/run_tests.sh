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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 auth_tests.test_auth_backends_llm.ModelBackendMissingCredentialsTests.setUp auth_tests.test_auth_backends_llm.ModelBackendMissingCredentialsTests.test_authenticate_wrapper_with_missing_credentials auth_tests.test_auth_backends_llm.ModelBackendMissingCredentialsTests.test_empty_kwargs_direct_backend_authenticate auth_tests.test_auth_backends_llm.ModelBackendMissingCredentialsTests.test_no_arguments_direct_backend_authenticate auth_tests.test_auth_backends_llm.ModelBackendMissingCredentialsTests.test_password_present_but_username_missing_direct auth_tests.test_auth_backends_llm.ModelBackendMissingCredentialsTests.test_unknown_kwarg_name_for_username_direct auth_tests.test_auth_backends_llm.ModelBackendMissingCredentialsTests.test_username_arg_present_but_password_missing_direct auth_tests.test_auth_backends_llm.ModelBackendMissingCredentialsTests.test_username_field_key_in_kwargs_is_none_direct auth_tests.test_auth_backends_llm.ModelBackendMissingCredentialsTests.test_username_none_password_none_explicit_direct auth_tests.test_auth_backends_llm.ModelBackendMissingCredentialsTests.test_username_none_password_present_direct auth_tests.test_auth_backends_llm.ModelBackendMissingCredentialsTests.test_username_provided_password_none_direct
coverage json -o coverage.json
: '>>>>> End Test Output'
