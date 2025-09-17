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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 auth_tests.test_auth_backends_llm.AdditionalAuthenticateNoneTests.setUpTestData auth_tests.test_auth_backends_llm.AdditionalAuthenticateNoneTests.test_custom_user_username_field_none_in_kwargs_does_not_query_or_hash auth_tests.test_auth_backends_llm.AdditionalAuthenticateNoneTests.test_custom_user_username_field_present_calls_get_by_natural_key auth_tests.test_auth_backends_llm.AdditionalAuthenticateNoneTests.test_explicit_password_none_does_not_query_or_hash auth_tests.test_auth_backends_llm.AdditionalAuthenticateNoneTests.test_explicit_username_none_does_not_query_or_hash auth_tests.test_auth_backends_llm.AdditionalAuthenticateNoneTests.test_missing_password_kwarg_does_not_query_or_hash auth_tests.test_auth_backends_llm.AdditionalAuthenticateNoneTests.test_missing_username_kwarg_does_not_query_or_hash auth_tests.test_auth_backends_llm.AdditionalAuthenticateNoneTests.test_no_credentials_does_not_query_or_hash auth_tests.test_auth_backends_llm.AdditionalAuthenticateNoneTests.test_request_only_authenticate_does_not_query_or_hash auth_tests.test_auth_backends_llm.AdditionalAuthenticateNoneTests.test_unrelated_kwarg_name_is_ignored_and_does_not_query
coverage json -o coverage.json
: '>>>>> End Test Output'
