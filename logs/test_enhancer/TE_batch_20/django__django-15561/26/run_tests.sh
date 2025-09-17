#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 schema.tests_llm.test_alter_field_custom_non_db_attr_noop_binaryfield schema.tests_llm.test_alter_field_custom_non_db_attr_noop_charfield schema.tests_llm.test_alter_field_custom_non_db_attr_noop_datefield schema.tests_llm.test_alter_field_custom_non_db_attr_noop_datetimefield schema.tests_llm.test_alter_field_custom_non_db_attr_noop_decimalfield schema.tests_llm.test_alter_field_custom_non_db_attr_noop_integerfield schema.tests_llm.test_alter_field_custom_non_db_attr_noop_textfield schema.tests_llm.test_alter_field_custom_non_db_attr_noop_timefield schema.tests_llm.test_alter_field_custom_non_db_attr_noop_uuidfield
coverage json -o coverage.json
: '>>>>> End Test Output'
