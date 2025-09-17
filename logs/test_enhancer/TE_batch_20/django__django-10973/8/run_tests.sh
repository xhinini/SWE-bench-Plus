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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 dbshell.test_postgresql_llm.PostgreSqlDbshellAdditionalTests._run_and_get_pgpassword dbshell.test_postgresql_llm.PostgreSqlDbshellAdditionalTests.test_password_bool_converted_to_str dbshell.test_postgresql_llm.PostgreSqlDbshellAdditionalTests.test_password_bytearray_converted_to_str dbshell.test_postgresql_llm.PostgreSqlDbshellAdditionalTests.test_password_bytes_converted_to_str dbshell.test_postgresql_llm.PostgreSqlDbshellAdditionalTests.test_password_custom_object_converted_to_str dbshell.test_postgresql_llm.PostgreSqlDbshellAdditionalTests.test_password_float_converted_to_str dbshell.test_postgresql_llm.PostgreSqlDbshellAdditionalTests.test_password_int_converted_to_str dbshell.test_postgresql_llm.PostgreSqlDbshellAdditionalTests.test_password_list_converted_to_str dbshell.test_postgresql_llm.PostgreSqlDbshellAdditionalTests.test_password_single_item_dict_converted_to_str dbshell.test_postgresql_llm.PostgreSqlDbshellAdditionalTests.test_password_single_item_set_converted_to_str dbshell.test_postgresql_llm.PostgreSqlDbshellAdditionalTests.test_password_tuple_converted_to_str
coverage json -o coverage.json
: '>>>>> End Test Output'
