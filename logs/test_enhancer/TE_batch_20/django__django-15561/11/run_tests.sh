#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 schema.tests_llm.test_alter_field_custom_non_db_attr_copy_and_modify schema.tests_llm.test_alter_field_custom_non_db_attr_multiple_attrs_noop schema.tests_llm.test_alter_field_custom_non_db_attr_new_has_extra_non_db schema.tests_llm.test_alter_field_custom_non_db_attr_noop_old_custom_new_plain schema.tests_llm.test_alter_field_custom_non_db_attr_noop_plain_new_custom schema.tests_llm.test_alter_field_custom_non_db_attr_noop_same_class schema.tests_llm.test_alter_field_custom_non_db_attr_old_and_new_share_name schema.tests_llm.test_alter_field_custom_non_db_attr_old_has_extra_non_db schema.tests_llm.test_alter_field_two_custom_attrs_noop_different_classes
coverage json -o coverage.json
: '>>>>> End Test Output'
