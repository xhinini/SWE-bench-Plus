#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 apps.tests_llm.ClearCacheSwappableTests._populate_swappable_cache apps.tests_llm.ClearCacheSwappableTests.test_clear_cache_clears_swappable_cache_direct apps.tests_llm.ClearCacheSwappableTests.test_clear_cache_clears_swappable_cache_when_not_ready apps.tests_llm.ClearCacheSwappableTests.test_clear_cache_during_available_unavailable_sequence apps.tests_llm.ClearCacheSwappableTests.test_clear_cache_is_idempotent apps.tests_llm.ClearCacheSwappableTests.test_register_model_clears_swappable_cache apps.tests_llm.ClearCacheSwappableTests.test_set_available_apps_clears_swappable_cache apps.tests_llm.ClearCacheSwappableTests.test_set_installed_apps_clears_swappable_cache apps.tests_llm.ClearCacheSwappableTests.test_unset_available_apps_clears_swappable_cache apps.tests_llm.ClearCacheSwappableTests.test_unset_installed_apps_clears_swappable_cache
coverage json -o coverage.json
: '>>>>> End Test Output'
