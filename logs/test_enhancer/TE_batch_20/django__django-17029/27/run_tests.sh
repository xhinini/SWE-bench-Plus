#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 apps.tests_llm.SwappableSettingsCacheTests.setUp apps.tests_llm.SwappableSettingsCacheTests.test_clear_after_populating_via_different_strings apps.tests_llm.SwappableSettingsCacheTests.test_clear_clears_entries_created_by_repeated_calls apps.tests_llm.SwappableSettingsCacheTests.test_clear_clears_multiple_cached_keys_for_different_casings apps.tests_llm.SwappableSettingsCacheTests.test_clear_clears_swappable_cache_after_get_models apps.tests_llm.SwappableSettingsCacheTests.test_clear_clears_swappable_cache_when_populated apps.tests_llm.SwappableSettingsCacheTests.test_clear_clears_when_apps_not_ready apps.tests_llm.SwappableSettingsCacheTests.test_clear_following_get_models_and_expire_cache_cycle apps.tests_llm.SwappableSettingsCacheTests.test_clear_is_idempotent apps.tests_llm.SwappableSettingsCacheTests.test_clear_when_not_populated_leaves_cache_empty apps.tests_llm.SwappableSettingsCacheTests.test_recomputed_after_clear
coverage json -o coverage.json
: '>>>>> End Test Output'
