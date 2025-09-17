#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 admin_checks.tests_llm.test_readonly_missing_field_message_for_index_zero_and_different_admin_name admin_checks.tests_llm.test_readonly_missing_field_message_includes_field_name_index_two admin_checks.tests_llm.test_readonly_missing_field_message_multiple_missing_fields admin_checks.tests_llm.test_readonly_missing_field_message_on_custom_inline_class admin_checks.tests_llm.test_readonly_missing_field_message_on_inline_index_one admin_checks.tests_llm.test_readonly_missing_field_message_tuple_single_item admin_checks.tests_llm.test_readonly_missing_field_message_when_model_has_similar_attr admin_checks.tests_llm.test_readonly_missing_field_message_with_admin_dynamic_getattr admin_checks.tests_llm.test_readonly_missing_field_message_with_mixed_types
coverage json -o coverage.json
: '>>>>> End Test Output'
