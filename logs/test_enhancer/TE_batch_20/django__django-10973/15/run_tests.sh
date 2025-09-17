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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 dbshell.test_postgresql_llm.AdditionalPostgreSqlDbshellTests._run_it dbshell.test_postgresql_llm.AdditionalPostgreSqlDbshellTests.test_password_bool_true dbshell.test_postgresql_llm.AdditionalPostgreSqlDbshellTests.test_password_bytes dbshell.test_postgresql_llm.AdditionalPostgreSqlDbshellTests.test_password_custom_object dbshell.test_postgresql_llm.AdditionalPostgreSqlDbshellTests.test_password_int dbshell.test_postgresql_llm.AdditionalPostgreSqlDbshellTests.test_password_list dbshell.test_postgresql_llm.AdditionalPostgreSqlDbshellTests.test_password_memoryview dbshell.test_postgresql_llm.AdditionalPostgreSqlDbshellTests.test_password_tuple dbshell.test_postgresql_llm.AdditionalPostgreSqlDbshellTests.test_pgpassword_is_str_instance
coverage json -o coverage.json
: '>>>>> End Test Output'
