#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 auth_tests.test_forms_llm.ReadOnlyPasswordHashExtraTests.test_bound_field_id_for_label_ignored_when_auto_id_present auth_tests.test_forms_llm.ReadOnlyPasswordHashExtraTests.test_field_label_tag_in_form_as_p_has_no_for_attribute auth_tests.test_forms_llm.ReadOnlyPasswordHashExtraTests.test_id_for_label_returns_none_with_custom_id auth_tests.test_forms_llm.ReadOnlyPasswordHashExtraTests.test_label_tag_with_custom_label_text_has_no_for_attribute auth_tests.test_forms_llm.ReadOnlyPasswordHashExtraTests.test_label_tag_with_label_suffix_ignored
coverage json -o coverage.json
: '>>>>> End Test Output'
