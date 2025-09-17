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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 dbshell.test_postgresql_llm.PostgreSqlDbshellCommandTestCase._run_it dbshell.test_postgresql_llm.PostgreSqlDbshellCommandTestCase.test_password_bool_true dbshell.test_postgresql_llm.PostgreSqlDbshellCommandTestCase.test_password_bytearray dbshell.test_postgresql_llm.PostgreSqlDbshellCommandTestCase.test_password_bytes dbshell.test_postgresql_llm.PostgreSqlDbshellCommandTestCase.test_password_custom_object dbshell.test_postgresql_llm.PostgreSqlDbshellCommandTestCase.test_password_custom_unicode_object dbshell.test_postgresql_llm.PostgreSqlDbshellCommandTestCase.test_password_decimal dbshell.test_postgresql_llm.PostgreSqlDbshellCommandTestCase.test_password_float dbshell.test_postgresql_llm.PostgreSqlDbshellCommandTestCase.test_password_fraction dbshell.test_postgresql_llm.PostgreSqlDbshellCommandTestCase.test_password_int
coverage json -o coverage.json
: '>>>>> End Test Output'
