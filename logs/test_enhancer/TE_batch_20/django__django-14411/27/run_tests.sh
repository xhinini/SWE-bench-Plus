#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 auth_tests.test_forms_llm.ReadOnlyPasswordHashWidgetIdForLabelTests.test_bound_field_custom_label_has_no_for_attribute auth_tests.test_forms_llm.ReadOnlyPasswordHashWidgetIdForLabelTests.test_bound_field_label_tag_has_no_for_attribute auth_tests.test_forms_llm.ReadOnlyPasswordHashWidgetIdForLabelTests.test_form_as_table_does_not_emit_for_attribute_for_hash_field auth_tests.test_forms_llm.ReadOnlyPasswordHashWidgetIdForLabelTests.test_label_tag_contains_no_for_even_if_id_provided
coverage json -o coverage.json
: '>>>>> End Test Output'
