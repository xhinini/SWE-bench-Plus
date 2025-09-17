#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 auth_tests.test_forms_llm.ReadOnlyPasswordHashIdForLabelDBTests.setUpTestData auth_tests.test_forms_llm.ReadOnlyPasswordHashIdForLabelDBTests.test_bound_field_widget_method_used_directly auth_tests.test_forms_llm.ReadOnlyPasswordHashIdForLabelDBTests.test_userchangeform_password_label_has_no_for_attribute_in_as_p auth_tests.test_forms_llm.ReadOnlyPasswordHashIdForLabelDBTests.test_userchangeform_password_label_in_as_table_no_for auth_tests.test_forms_llm.ReadOnlyPasswordHashIdForLabelSimpleTests.test_unbound_field_widget_id_for_label_returns_none
coverage json -o coverage.json
: '>>>>> End Test Output'
