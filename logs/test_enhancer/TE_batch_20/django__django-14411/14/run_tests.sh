#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 auth_tests.test_forms_llm.ReadOnlyPasswordHashIdForLabelTests.test_id_for_label_on_bound_field_delegates_to_widget_and_returns_none auth_tests.test_forms_llm.ReadOnlyPasswordHashIdForLabelTests.test_label_tag_with_attrs_and_contents_has_no_for auth_tests.test_forms_llm.ReadOnlyPasswordHashIdForLabelTests.test_label_tag_with_contents_override
coverage json -o coverage.json
: '>>>>> End Test Output'
