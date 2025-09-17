#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 auth_tests.test_forms_llm.ReadOnlyPasswordHashWidgetIdForLabelTests.test_label_tag_with_explicit_contents_has_no_for auth_tests.test_forms_llm.ReadOnlyPasswordHashWidgetIntegrationTests.setUpTestData
coverage json -o coverage.json
: '>>>>> End Test Output'
