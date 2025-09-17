#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 admin_checks.tests_llm.test_readonly_missing_field_dynamic_getattr_admin admin_checks.tests_llm.test_readonly_missing_field_field_name_with_digits admin_checks.tests_llm.test_readonly_missing_field_in_stacked_inline_includes_field_name admin_checks.tests_llm.test_readonly_missing_field_includes_field_name_inline_custom_class admin_checks.tests_llm.test_readonly_missing_field_includes_field_name_modeladmin_variant1 admin_checks.tests_llm.test_readonly_missing_field_includes_field_name_modeladmin_variant2 admin_checks.tests_llm.test_readonly_missing_field_includes_field_name_on_different_model admin_checks.tests_llm.test_readonly_missing_field_index_two_reports_correct_label admin_checks.tests_llm.test_readonly_missing_field_with_callable_present_in_sequence
coverage json -o coverage.json
: '>>>>> End Test Output'
