#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 apps.tests_llm.ClearCacheRegressionTests.test_clear_cache_after_multiple_gets apps.tests_llm.ClearCacheRegressionTests.test_clear_cache_after_registering_additional_model apps.tests_llm.ClearCacheRegressionTests.test_clear_cache_after_repeated_model_registration apps.tests_llm.ClearCacheRegressionTests.test_clear_cache_after_swappable_queries_with_different_casing apps.tests_llm.ClearCacheRegressionTests.test_clear_cache_after_swapped_and_swappable_calls apps.tests_llm.ClearCacheRegressionTests.test_clear_cache_clears_swappable_and_models apps.tests_llm.ClearCacheRegressionTests.test_clear_cache_idempotent apps.tests_llm.ClearCacheRegressionTests.test_clear_cache_when_models_populated_after_swappable apps.tests_llm.ClearCacheRegressionTests.test_clear_cache_when_models_populated_before_swappable apps.tests_llm.ClearCacheRegressionTests.test_clear_cache_with_multiple_swappable_models
coverage json -o coverage.json
: '>>>>> End Test Output'
