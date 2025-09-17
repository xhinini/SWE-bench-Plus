#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 schema.tests_llm.test_alter_binaryfield_custom_non_db_attr_noop schema.tests_llm.test_alter_booleanfield_custom_non_db_attr_noop schema.tests_llm.test_alter_charfield_custom_non_db_attr_noop schema.tests_llm.test_alter_datetimefield_custom_non_db_attr_noop schema.tests_llm.test_alter_decimalfield_custom_non_db_attr_noop schema.tests_llm.test_alter_durationfield_custom_non_db_attr_noop schema.tests_llm.test_alter_genericipaddressfield_custom_non_db_attr_noop schema.tests_llm.test_alter_integerfield_custom_non_db_attr_noop schema.tests_llm.test_alter_textfield_custom_non_db_attr_noop schema.tests_llm.test_alter_uuidfield_custom_non_db_attr_noop
coverage json -o coverage.json
: '>>>>> End Test Output'
