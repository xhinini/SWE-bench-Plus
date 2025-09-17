#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 apps.tests_llm.ClearCacheRegressionTests.assert_both_caches_cleared apps.tests_llm.ClearCacheRegressionTests.make_registry apps.tests_llm.ClearCacheRegressionTests.test_clear_cache_after_repopulation apps.tests_llm.ClearCacheRegressionTests.test_clear_cache_direct apps.tests_llm.ClearCacheRegressionTests.test_clear_cache_multiple_times apps.tests_llm.ClearCacheRegressionTests.test_clear_cache_normalizes_input_case apps.tests_llm.ClearCacheRegressionTests.test_clear_cache_on_non_main_registry apps.tests_llm.ClearCacheRegressionTests.test_clear_cache_via_set_and_unset_installed_apps apps.tests_llm.ClearCacheRegressionTests.test_clear_cache_via_set_available_apps apps.tests_llm.ClearCacheRegressionTests.test_clear_cache_via_unset_available_apps apps.tests_llm.ClearCacheRegressionTests.test_clear_cache_when_ready_false apps.tests_llm.ClearCacheRegressionTests.test_clear_cache_with_pending_operations
coverage json -o coverage.json
: '>>>>> End Test Output'
