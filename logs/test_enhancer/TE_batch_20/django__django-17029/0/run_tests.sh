#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 apps.tests_llm.ClearCacheSwappableTests.test_clear_cache_after_get_models_then_swappable apps.tests_llm.ClearCacheSwappableTests.test_clear_cache_clears_swappable_after_call apps.tests_llm.ClearCacheSwappableTests.test_clear_cache_does_not_repopulate_swappable_via_expire apps.tests_llm.ClearCacheSwappableTests.test_clear_cache_during_set_unset_available_apps apps.tests_llm.ClearCacheSwappableTests.test_clear_cache_during_set_unset_installed_apps apps.tests_llm.ClearCacheSwappableTests.test_clear_cache_multiple_times_is_idempotent apps.tests_llm.ClearCacheSwappableTests.test_clear_cache_when_not_ready_does_not_error_and_clears apps.tests_llm.ClearCacheSwappableTests.test_register_model_triggers_clear_cache apps.tests_llm.ClearCacheSwappableTests.test_swappable_cache_case_insensitivity_and_clear
coverage json -o coverage.json
: '>>>>> End Test Output'
