#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 schema.tests_llm.NonDBAttrsRegressionTests.test_both_fields_custom_attr_different_values_ignored schema.tests_llm.NonDBAttrsRegressionTests.test_custom_attr_on_binaryfield_ignored schema.tests_llm.NonDBAttrsRegressionTests.test_custom_attr_on_slugfield_ignored schema.tests_llm.NonDBAttrsRegressionTests.test_custom_attr_only_on_old_field_ignored_when_other_non_db_attr_changes schema.tests_llm.NonDBAttrsRegressionTests.test_custom_attr_present_only_in_new_and_also_other_non_db_change schema.tests_llm.NonDBAttrsRegressionTests.test_multiple_custom_attrs_ignored schema.tests_llm.NonDBAttrsRegressionTests.test_new_field_only_custom_attr_ignored schema.tests_llm.NonDBAttrsRegressionTests.test_old_field_only_custom_attr_ignored schema.tests_llm.NonDBAttrsRegressionTests.test_two_distinct_custom_attrs_in_different_fields_ignored
coverage json -o coverage.json
: '>>>>> End Test Output'
