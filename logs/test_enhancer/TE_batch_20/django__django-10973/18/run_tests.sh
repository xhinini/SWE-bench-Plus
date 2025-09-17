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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 dbshell.test_postgresql_llm.PostgresPasswordConversionTests._assert_password_converted dbshell.test_postgresql_llm.PostgresPasswordConversionTests._run_it dbshell.test_postgresql_llm.PostgresPasswordConversionTests.test_password_bool_converted dbshell.test_postgresql_llm.PostgresPasswordConversionTests.test_password_bytearray_converted dbshell.test_postgresql_llm.PostgresPasswordConversionTests.test_password_bytes_converted dbshell.test_postgresql_llm.PostgresPasswordConversionTests.test_password_bytes_with_nonascii_converted dbshell.test_postgresql_llm.PostgresPasswordConversionTests.test_password_complex_converted dbshell.test_postgresql_llm.PostgresPasswordConversionTests.test_password_custom_object_converted dbshell.test_postgresql_llm.PostgresPasswordConversionTests.test_password_float_converted dbshell.test_postgresql_llm.PostgresPasswordConversionTests.test_password_int_converted dbshell.test_postgresql_llm.PostgresPasswordConversionTests.test_password_list_converted dbshell.test_postgresql_llm.PostgresPasswordConversionTests.test_password_tuple_converted
coverage json -o coverage.json
: '>>>>> End Test Output'
