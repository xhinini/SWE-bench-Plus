#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 basic.tests_llm.ManagerWrapsRegressionTests._assert_manager_matches_queryset basic.tests_llm.ManagerWrapsRegressionTests.test_aggregate_wrapper basic.tests_llm.ManagerWrapsRegressionTests.test_annotate_wrapper basic.tests_llm.ManagerWrapsRegressionTests.test_bulk_create_wrapper basic.tests_llm.ManagerWrapsRegressionTests.test_count_wrapper basic.tests_llm.ManagerWrapsRegressionTests.test_exists_wrapper basic.tests_llm.ManagerWrapsRegressionTests.test_filter_wrapper basic.tests_llm.ManagerWrapsRegressionTests.test_get_wrapper basic.tests_llm.ManagerWrapsRegressionTests.test_update_wrapper basic.tests_llm.ManagerWrapsRegressionTests.test_values_list_wrapper basic.tests_llm.ManagerWrapsRegressionTests.test_values_wrapper
coverage json -o coverage.json
: '>>>>> End Test Output'
