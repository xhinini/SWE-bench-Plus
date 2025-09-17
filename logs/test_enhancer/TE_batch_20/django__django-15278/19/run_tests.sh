#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 schema.tests_llm.TestAddFieldSqliteOnly.test_add_binary_field_sqlite_no_attr_error schema.tests_llm.TestAddFieldSqliteOnly.test_add_boolean_field_sqlite_no_attr_error schema.tests_llm.TestAddFieldSqliteOnly.test_add_char_field_sqlite_no_attr_error schema.tests_llm.TestAddFieldSqliteOnly.test_add_datefield_auto_now_sqlite_no_attr_error schema.tests_llm.TestAddFieldSqliteOnly.test_add_decimalfield_sqlite_no_attr_error schema.tests_llm.TestAddFieldSqliteOnly.test_add_durationfield_with_default_sqlite_no_attr_error schema.tests_llm.TestAddFieldSqliteOnly.test_add_floatfield_sqlite_no_attr_error schema.tests_llm.TestAddFieldSqliteOnly.test_add_integer_field_sqlite_no_attr_error schema.tests_llm.TestAddFieldSqliteOnly.test_add_textfield_unhashable_default_sqlite_no_attr_error schema.tests_llm.TestAddFieldSqliteOnly.test_add_timefield_auto_now_add_sqlite_no_attr_error
coverage json -o coverage.json
: '>>>>> End Test Output'
