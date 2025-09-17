#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 apps.tests_llm.ClearCacheSwappableTests.test_clear_cache_after_get_models_call apps.tests_llm.ClearCacheSwappableTests.test_clear_cache_clears_after_populated_by_expire_only apps.tests_llm.ClearCacheSwappableTests.test_clear_cache_clears_multiple_keys apps.tests_llm.ClearCacheSwappableTests.test_clear_cache_clears_swappable_cache_when_expire_repopulates apps.tests_llm.ClearCacheSwappableTests.test_clear_cache_idempotent apps.tests_llm.ClearCacheSwappableTests.test_clear_cache_when_expire_calls_multiple_keys apps.tests_llm.ClearCacheSwappableTests.test_clear_cache_when_not_ready_still_clears_swappable_cache apps.tests_llm.ClearCacheSwappableTests.test_clear_cache_with_mixed_models apps.tests_llm.ClearCacheSwappableTests.test_clear_cache_with_no_models_clears_existing_swappable_cache apps.tests_llm.make_fake_app_config apps.tests_llm.make_fake_model
coverage json -o coverage.json
: '>>>>> End Test Output'
