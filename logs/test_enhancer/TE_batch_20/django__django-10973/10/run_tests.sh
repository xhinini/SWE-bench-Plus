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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 dbshell.test_postgresql_llm.PostgreSqlDbshellCommandTestCase._capture_run_env dbshell.test_postgresql_llm.PostgreSqlDbshellCommandTestCase._run_it dbshell.test_postgresql_llm.PostgreSqlDbshellCommandTestCase.test_password_bool_is_converted_to_str_in_env dbshell.test_postgresql_llm.PostgreSqlDbshellCommandTestCase.test_password_bytes_is_converted_to_str_in_env dbshell.test_postgresql_llm.PostgreSqlDbshellCommandTestCase.test_password_int_is_converted_to_str_in_env dbshell.test_postgresql_llm.PostgreSqlDbshellCommandTestCase.test_password_list_is_converted_to_str_in_env dbshell.test_postgresql_llm.PostgreSqlDbshellCommandTestCase.test_password_object_is_converted_to_str_in_env dbshell.test_postgresql_llm.PostgreSqlDbshellCommandTestCase.test_sigint_handler
coverage json -o coverage.json
: '>>>>> End Test Output'
