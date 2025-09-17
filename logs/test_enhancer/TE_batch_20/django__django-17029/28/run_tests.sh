#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 apps.tests_llm.ClearCacheRegressionTests._make_dummy_model apps.tests_llm.ClearCacheRegressionTests.test_clear_cache_after_register_model apps.tests_llm.ClearCacheRegressionTests.test_clear_cache_clears_swappable_simple apps.tests_llm.ClearCacheRegressionTests.test_clear_cache_is_idempotent apps.tests_llm.ClearCacheRegressionTests.test_clear_cache_resets_get_models_cache apps.tests_llm.ClearCacheRegressionTests.test_clear_cache_with_expire_side_effect_does_not_leave_swappable_cached apps.tests_llm.ClearCacheRegressionTests.test_clear_cache_with_swappable_model_entry apps.tests_llm.ClearCacheRegressionTests.test_set_available_apps_clears_swappable_cache apps.tests_llm.ClearCacheRegressionTests.test_set_installed_apps_clears_swappable_cache_and_restores_on_unset apps.tests_llm.ClearCacheRegressionTests.test_unset_available_apps_restores_and_clears_cache
coverage json -o coverage.json
: '>>>>> End Test Output'
