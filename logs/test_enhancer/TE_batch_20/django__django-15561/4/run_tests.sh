#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 schema.tests_llm.test_alter_field_custom_non_db_attr_noop_1 schema.tests_llm.test_alter_field_custom_non_db_attr_noop_10 schema.tests_llm.test_alter_field_custom_non_db_attr_noop_2 schema.tests_llm.test_alter_field_custom_non_db_attr_noop_3 schema.tests_llm.test_alter_field_custom_non_db_attr_noop_4 schema.tests_llm.test_alter_field_custom_non_db_attr_noop_5 schema.tests_llm.test_alter_field_custom_non_db_attr_noop_6 schema.tests_llm.test_alter_field_custom_non_db_attr_noop_7 schema.tests_llm.test_alter_field_custom_non_db_attr_noop_8 schema.tests_llm.test_alter_field_custom_non_db_attr_noop_9
coverage json -o coverage.json
: '>>>>> End Test Output'
