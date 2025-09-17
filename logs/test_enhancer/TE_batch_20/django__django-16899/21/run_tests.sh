#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 admin_checks.tests_llm.test_callable_in_readonly_fields_produces_no_error admin_checks.tests_llm.test_dynamic_attribute_on_modeladmin_produces_no_error admin_checks.tests_llm.test_error_message_includes_admin_class_name_correctly admin_checks.tests_llm.test_inline_error_uses_correct_model_label_and_field_name admin_checks.tests_llm.test_multiple_missing_readonly_fields_all_listed admin_checks.tests_llm.test_nonexistent_field_includes_field_name_index0 admin_checks.tests_llm.test_nonexistent_field_includes_field_name_index2 admin_checks.tests_llm.test_nonexistent_field_on_custom_inline_includes_field_name admin_checks.tests_llm.test_nonexistent_field_with_list_type_includes_field_name admin_checks.tests_llm.test_readonly_field_that_is_model_method_produces_no_error
coverage json -o coverage.json
: '>>>>> End Test Output'
