#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 apps.tests_llm.AppsSwappableCacheTests.make_model apps.tests_llm.AppsSwappableCacheTests.test_clear_cache_after_get_models_populated apps.tests_llm.AppsSwappableCacheTests.test_clear_cache_cache_info_zeroed apps.tests_llm.AppsSwappableCacheTests.test_clear_cache_detects_new_swappable_model apps.tests_llm.AppsSwappableCacheTests.test_clear_cache_multiple_calls_idempotent apps.tests_llm.AppsSwappableCacheTests.test_clear_cache_reflects_removal_of_swappable_attribute apps.tests_llm.AppsSwappableCacheTests.test_clear_cache_respects_label_case_insensitivity apps.tests_llm.AppsSwappableCacheTests.test_clear_cache_updates_swappable_value_changed apps.tests_llm.AppsSwappableCacheTests.test_clear_cache_updates_swapped_removed apps.tests_llm.AppsSwappableCacheTests.test_clear_cache_with_multiple_models_updates_result_correctly apps.tests_llm.AppsSwappableCacheTests.test_get_swappable_uses_swapped_priority
coverage json -o coverage.json
: '>>>>> End Test Output'
