#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 admin_checks.tests_llm.test_inherited_modeladmin_nonexistent_field_message admin_checks.tests_llm.test_multiple_readonly_fields_second_index_message admin_checks.tests_llm.test_nonexistent_field_complex_class_name_message admin_checks.tests_llm.test_nonexistent_field_index_zero_message admin_checks.tests_llm.test_nonexistent_field_list_type_message admin_checks.tests_llm.test_nonexistent_field_on_tabular_inline_message admin_checks.tests_llm.test_readonly_callable_no_error admin_checks.tests_llm.test_readonly_field_on_model_attribute_no_error admin_checks.tests_llm.test_readonly_fields_from_property_message admin_checks.tests_llm.test_tabular_inline_classname_in_message
coverage json -o coverage.json
: '>>>>> End Test Output'
