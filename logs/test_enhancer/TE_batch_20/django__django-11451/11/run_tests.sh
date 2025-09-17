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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 auth_tests.test_auth_backends_llm.ModelBackendAuthenticateMissingCredentialsTests.setUpTestData auth_tests.test_auth_backends_llm.ModelBackendAuthenticateMissingCredentialsTests.test_empty_username_and_password_triggers_set_password_and_query
coverage json -o coverage.json
: '>>>>> End Test Output'
