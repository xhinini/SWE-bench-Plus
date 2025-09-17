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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 auth_tests.test_auth_backends_llm.AuthenticateIncompleteCredentialsTests.setUp auth_tests.test_auth_backends_llm.AuthenticateIncompleteCredentialsTests.test_authenticate_with_custom_username_field_and_password_returns_user auth_tests.test_auth_backends_llm.AuthenticateIncompleteCredentialsTests.test_username_field_in_kwargs_with_missing_password_no_db_or_hash auth_tests.test_auth_backends_llm.CountingMD5PasswordHasher.encode auth_tests.test_auth_backends_llm.CountingMD5PasswordHasher.harden_runtime auth_tests.test_auth_backends_llm.CountingMD5PasswordHasher.must_update auth_tests.test_auth_backends_llm.CountingMD5PasswordHasher.salt auth_tests.test_auth_backends_llm.CountingMD5PasswordHasher.verify
coverage json -o coverage.json
: '>>>>> End Test Output'
