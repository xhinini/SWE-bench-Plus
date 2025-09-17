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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 dbshell.test_postgresql_llm.test_bytearray_password_is_strified dbshell.test_postgresql_llm.test_bytes_password_is_strified dbshell.test_postgresql_llm.test_custom_object_password_is_strified dbshell.test_postgresql_llm.test_float_password_is_strified dbshell.test_postgresql_llm.test_int_password_is_strified dbshell.test_postgresql_llm.test_nonascii_bytes_password_is_strified dbshell.test_postgresql_llm.test_os_environ_not_polluted_with_password_types dbshell.test_postgresql_llm.test_plain_object_password_is_strified dbshell.test_postgresql_llm.test_port_as_int_and_password_int dbshell.test_postgresql_llm.test_sigint_restored_on_calledprocesserror_with_nonstr_password
coverage json -o coverage.json
: '>>>>> End Test Output'
