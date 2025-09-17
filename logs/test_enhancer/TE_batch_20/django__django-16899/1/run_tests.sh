#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 admin_checks.tests_llm.test_readonly_missing_field_custom_admin_name admin_checks.tests_llm.test_readonly_missing_field_dynamic_class_name admin_checks.tests_llm.test_readonly_missing_field_index_zero_modeladmin_list admin_checks.tests_llm.test_readonly_missing_field_inline_multiple_indices admin_checks.tests_llm.test_readonly_missing_field_on_different_model admin_checks.tests_llm.test_readonly_multiple_missing_fields_modeladmin admin_checks.tests_llm.test_readonly_nonexistent_index_one_modeladmin admin_checks.tests_llm.test_readonly_nonexistent_list_modeladmin admin_checks.tests_llm.test_readonly_nonexistent_stacked_inline admin_checks.tests_llm.test_readonly_nonexistent_tabular_inline
coverage json -o coverage.json
: '>>>>> End Test Output'
