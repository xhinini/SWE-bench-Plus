#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 apps.tests_llm.ClearCacheRegressionTests.test_clear_cache_clears_swappable_cache_basic apps.tests_llm.ClearCacheRegressionTests.test_clear_cache_does_not_affect_other_registry_instances apps.tests_llm.ClearCacheRegressionTests.test_clear_cache_during_get_models_repopulation apps.tests_llm.ClearCacheRegressionTests.test_clear_cache_idempotent apps.tests_llm.ClearCacheRegressionTests.test_clear_cache_preserves_ready_flag_and_clears_caches apps.tests_llm.ClearCacheRegressionTests.test_clear_cache_when_not_ready_clears_swappable apps.tests_llm.ClearCacheRegressionTests.test_clear_cache_with_multiple_repopulating_configs apps.tests_llm.ClearCacheRegressionTests.test_get_swappable_recomputed_after_clear apps.tests_llm.ClearCacheRegressionTests.test_register_model_triggers_clear_cache_on_registry
coverage json -o coverage.json
: '>>>>> End Test Output'
