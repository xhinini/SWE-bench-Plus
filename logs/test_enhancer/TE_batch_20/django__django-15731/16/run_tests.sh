#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 basic.tests_llm.ManagerWrapsRegressionTests.test_from_queryset_creates_methods_with_correct_signature_and_wrapped basic.tests_llm.ManagerWrapsRegressionTests.test_inspect_signature_matches_queryset_for_bulk_create basic.tests_llm.ManagerWrapsRegressionTests.test_inspect_signature_matches_queryset_for_filter basic.tests_llm.ManagerWrapsRegressionTests.test_manager_calls_underlying_queryset_method_correctly basic.tests_llm.ManagerWrapsRegressionTests.test_manager_method_has_same_signature_string_as_queryset_for_update
coverage json -o coverage.json
: '>>>>> End Test Output'
