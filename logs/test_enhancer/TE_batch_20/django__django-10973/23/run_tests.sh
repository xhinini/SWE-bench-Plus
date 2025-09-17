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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 dbshell.test_postgresql_llm.PostgreSqlPasswordConversionTests._run_it dbshell.test_postgresql_llm.PostgreSqlPasswordConversionTests.test_password_bool_true_is_converted_to_str dbshell.test_postgresql_llm.PostgreSqlPasswordConversionTests.test_password_bytearray_is_converted_to_str dbshell.test_postgresql_llm.PostgreSqlPasswordConversionTests.test_password_bytes_is_converted_to_str dbshell.test_postgresql_llm.PostgreSqlPasswordConversionTests.test_password_complex_is_converted_to_str dbshell.test_postgresql_llm.PostgreSqlPasswordConversionTests.test_password_decimal_is_converted_to_str dbshell.test_postgresql_llm.PostgreSqlPasswordConversionTests.test_password_float_is_converted_to_str dbshell.test_postgresql_llm.PostgreSqlPasswordConversionTests.test_password_frozenset_is_converted_to_str dbshell.test_postgresql_llm.PostgreSqlPasswordConversionTests.test_password_int_is_converted_to_str dbshell.test_postgresql_llm.PostgreSqlPasswordConversionTests.test_password_object_with___str___is_converted_to_str dbshell.test_postgresql_llm.PostgreSqlPasswordConversionTests.test_password_pathlike_is_converted_to_str
coverage json -o coverage.json
: '>>>>> End Test Output'
