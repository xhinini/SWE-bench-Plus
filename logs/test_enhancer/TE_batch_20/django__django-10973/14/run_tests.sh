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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 dbshell.test_postgresql_llm.test_empty_string_password_does_not_set_env dbshell.test_postgresql_llm.test_password_bool_true dbshell.test_postgresql_llm.test_password_bytearray dbshell.test_postgresql_llm.test_password_bytes dbshell.test_postgresql_llm.test_password_custom_object_str dbshell.test_postgresql_llm.test_password_custom_object_unicode_str dbshell.test_postgresql_llm.test_password_float dbshell.test_postgresql_llm.test_password_integer dbshell.test_postgresql_llm.test_password_large_integer dbshell.test_postgresql_llm.test_zero_password_does_not_set_env
coverage json -o coverage.json
: '>>>>> End Test Output'
