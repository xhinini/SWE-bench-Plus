#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 apps.tests_llm.ClearSwappableCacheTests.setUp apps.tests_llm.ClearSwappableCacheTests.test_clear_cache_after_set_available_apps apps.tests_llm.ClearSwappableCacheTests.test_clear_cache_after_set_installed_apps_unset apps.tests_llm.ClearSwappableCacheTests.test_clear_cache_clears_after_register_model_populates_swappable apps.tests_llm.ClearSwappableCacheTests.test_clear_cache_clears_swappable_after_models_cache apps.tests_llm.ClearSwappableCacheTests.test_clear_cache_clears_swappable_simple apps.tests_llm.ClearSwappableCacheTests.test_clear_cache_clears_swappable_when_not_ready apps.tests_llm.ClearSwappableCacheTests.test_clear_cache_is_idempotent apps.tests_llm.ClearSwappableCacheTests.test_clear_cache_multiple_swappable_keys apps.tests_llm.ClearSwappableCacheTests.test_clear_cache_with_model_expire_populates_swappable apps.tests_llm.ClearSwappableCacheTests.test_clear_cache_with_multiple_models_expire
coverage json -o coverage.json
: '>>>>> End Test Output'
