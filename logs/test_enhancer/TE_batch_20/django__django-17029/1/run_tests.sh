#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 apps.tests_llm.ClearCacheRegressionTests.test_clear_cache_case_insensitive_keys apps.tests_llm.ClearCacheRegressionTests.test_clear_cache_clears_after_get_models_then_swappable apps.tests_llm.ClearCacheRegressionTests.test_clear_cache_clears_multiple_swappable_entries apps.tests_llm.ClearCacheRegressionTests.test_clear_cache_clears_none_values apps.tests_llm.ClearCacheRegressionTests.test_clear_cache_does_not_raise_when_empty apps.tests_llm.ClearCacheRegressionTests.test_clear_cache_idempotent apps.tests_llm.ClearCacheRegressionTests.test_clear_cache_multiple_times_after_populate apps.tests_llm.ClearCacheRegressionTests.test_clear_cache_when_models_ready_false apps.tests_llm.ClearCacheRegressionTests.test_get_models_cache_cleared_after_clear_cache_multiple_calls apps.tests_llm.ClearCacheRegressionTests.test_get_swappable_cache_recomputed_after_clear
coverage json -o coverage.json
: '>>>>> End Test Output'
