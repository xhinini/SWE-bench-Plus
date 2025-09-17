#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 schema.tests_llm.AddFieldRegressionTests._create_author_table schema.tests_llm.AddFieldRegressionTests._get_column_names schema.tests_llm.AddFieldRegressionTests.test_add_nullable_booleanfield_no_attribute_error schema.tests_llm.AddFieldRegressionTests.test_add_nullable_charfield_no_attribute_error schema.tests_llm.AddFieldRegressionTests.test_add_nullable_datefield_no_attribute_error schema.tests_llm.AddFieldRegressionTests.test_add_nullable_datetimefield_no_attribute_error schema.tests_llm.AddFieldRegressionTests.test_add_nullable_decimalfield_no_attribute_error schema.tests_llm.AddFieldRegressionTests.test_add_nullable_floatfield_no_attribute_error schema.tests_llm.AddFieldRegressionTests.test_add_nullable_integer_field_no_attribute_error schema.tests_llm.AddFieldRegressionTests.test_add_textfield_no_attribute_error schema.tests_llm.AddFieldRegressionTests.test_adding_primary_key_field_triggers_table_remake
coverage json -o coverage.json
: '>>>>> End Test Output'
