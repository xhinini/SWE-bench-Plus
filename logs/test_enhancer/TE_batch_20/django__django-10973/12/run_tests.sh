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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 dbshell.test_postgresql_llm.PostgreSqlDbshellCommandExtendedTests._make_mock dbshell.test_postgresql_llm.PostgreSqlDbshellCommandExtendedTests.test_password_bool_is_string dbshell.test_postgresql_llm.PostgreSqlDbshellCommandExtendedTests.test_password_bytearray_is_string dbshell.test_postgresql_llm.PostgreSqlDbshellCommandExtendedTests.test_password_bytes_is_string dbshell.test_postgresql_llm.PostgreSqlDbshellCommandExtendedTests.test_password_custom_object_with_str_is_string dbshell.test_postgresql_llm.PostgreSqlDbshellCommandExtendedTests.test_password_empty_string_is_string dbshell.test_postgresql_llm.PostgreSqlDbshellCommandExtendedTests.test_password_int_is_string dbshell.test_postgresql_llm.PostgreSqlDbshellCommandExtendedTests.test_password_memoryview_is_string dbshell.test_postgresql_llm.PostgreSqlDbshellCommandExtendedTests.test_password_non_utf8_bytes_is_string dbshell.test_postgresql_llm.PostgreSqlDbshellCommandExtendedTests.test_password_pathlike_is_string
coverage json -o coverage.json
: '>>>>> End Test Output'
