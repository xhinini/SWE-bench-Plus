#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 apps.tests_llm.ClearCacheSwappableTests.tearDown apps.tests_llm.ClearCacheSwappableTests.test_clear_cache_after_set_installed_apps_and_unset apps.tests_llm.ClearCacheSwappableTests.test_clear_cache_after_unset_available_apps_restores_cleared_state apps.tests_llm.ClearCacheSwappableTests.test_clear_cache_during_models_not_ready apps.tests_llm.ClearCacheSwappableTests.test_clear_cache_handles_expire_that_repopulates_cache apps.tests_llm.ClearCacheSwappableTests.test_clear_cache_idempotent_and_remains_empty apps.tests_llm.ClearCacheSwappableTests.test_clear_cache_resets_swappable_cache_simple apps.tests_llm.ClearCacheSwappableTests.test_clear_cache_when_set_available_apps_is_called apps.tests_llm.ClearCacheSwappableTests.test_clear_cache_with_lazy_model_operation_and_expire apps.tests_llm.ClearCacheSwappableTests.test_clear_cache_with_multiple_models_repopulating
coverage json -o coverage.json
: '>>>>> End Test Output'
