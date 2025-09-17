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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 dbshell.test_postgresql_llm.PasswordTypeConversionTests._run_it dbshell.test_postgresql_llm.PasswordTypeConversionTests.test_bool_password_converted_to_str dbshell.test_postgresql_llm.PasswordTypeConversionTests.test_bytearray_password_converted_to_str dbshell.test_postgresql_llm.PasswordTypeConversionTests.test_bytes_password_converted_to_str dbshell.test_postgresql_llm.PasswordTypeConversionTests.test_bytes_with_non_ascii_converted_to_str dbshell.test_postgresql_llm.PasswordTypeConversionTests.test_custom_object_password_converted_via_str dbshell.test_postgresql_llm.PasswordTypeConversionTests.test_float_password_converted_to_str dbshell.test_postgresql_llm.PasswordTypeConversionTests.test_int_password_converted_to_str dbshell.test_postgresql_llm.PasswordTypeConversionTests.test_unicode_object_password_converted_via_str
coverage json -o coverage.json
: '>>>>> End Test Output'
