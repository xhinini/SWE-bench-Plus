#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 schema.tests_llm._make_custom_field_subclass schema.tests_llm.test_alter_binaryfield_with_custom_non_db_attr_noop schema.tests_llm.test_alter_booleanfield_with_custom_non_db_attr_noop schema.tests_llm.test_alter_charfield_with_custom_non_db_attr_noop schema.tests_llm.test_alter_datefield_with_custom_non_db_attr_noop schema.tests_llm.test_alter_datetimefield_with_custom_non_db_attr_noop schema.tests_llm.test_alter_decimalfield_with_custom_non_db_attr_noop schema.tests_llm.test_alter_integerfield_with_custom_non_db_attr_noop schema.tests_llm.test_alter_textfield_with_custom_non_db_attr_noop schema.tests_llm.test_alter_timefield_with_custom_non_db_attr_noop schema.tests_llm.test_alter_uuidfield_with_custom_non_db_attr_noop
coverage json -o coverage.json
: '>>>>> End Test Output'
