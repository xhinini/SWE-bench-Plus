#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 forms_tests.tests.test_formsets_llm.NonFormErrorsCachingTests._assert_cached_non_form_errors forms_tests.tests.test_formsets_llm.NonFormErrorsCachingTests.test_cached_after_accessing_errors_property forms_tests.tests.test_formsets_llm.NonFormErrorsCachingTests.test_cached_after_is_valid_call forms_tests.tests.test_formsets_llm.NonFormErrorsCachingTests.test_cached_for_empty_formset_bound forms_tests.tests.test_formsets_llm.NonFormErrorsCachingTests.test_cached_for_missing_management_form forms_tests.tests.test_formsets_llm.NonFormErrorsCachingTests.test_cached_for_valid_formset forms_tests.tests.test_formsets_llm.NonFormErrorsCachingTests.test_cached_for_validate_max forms_tests.tests.test_formsets_llm.NonFormErrorsCachingTests.test_cached_for_validate_min forms_tests.tests.test_formsets_llm.NonFormErrorsCachingTests.test_cached_when_absolute_max_exceeded forms_tests.tests.test_formsets_llm.NonFormErrorsCachingTests.test_cached_when_clean_raises
coverage json -o coverage.json
: '>>>>> End Test Output'
