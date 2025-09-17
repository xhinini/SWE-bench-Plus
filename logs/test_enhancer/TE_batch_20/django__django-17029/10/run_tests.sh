#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 apps.tests_llm.ClearCacheRegressionTests.setUp apps.tests_llm.ClearCacheRegressionTests.test_clear_cache_clears_case_insensitive_isolated apps.tests_llm.ClearCacheRegressionTests.test_clear_cache_clears_models_cache_main apps.tests_llm.ClearCacheRegressionTests.test_clear_cache_clears_multiple_entries_isolated apps.tests_llm.ClearCacheRegressionTests.test_clear_cache_clears_multiple_swappable_entries_main apps.tests_llm.ClearCacheRegressionTests.test_clear_cache_clears_swappable_and_models_isolated apps.tests_llm.ClearCacheRegressionTests.test_clear_cache_clears_swappable_cache_case_insensitive_main apps.tests_llm.ClearCacheRegressionTests.test_clear_cache_is_idempotent_main apps.tests_llm.ClearCacheRegressionTests.test_clear_cache_on_fresh_registry_no_error apps.tests_llm.ClearCacheRegressionTests.test_register_model_triggers_clear_of_swappable_cache
coverage json -o coverage.json
: '>>>>> End Test Output'
