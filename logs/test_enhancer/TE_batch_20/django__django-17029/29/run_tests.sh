#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 apps.tests_llm.ClearCacheSwappableTests.test_clear_cache_after_repopulation_during_expire apps.tests_llm.ClearCacheSwappableTests.test_clear_cache_clears_both_caches apps.tests_llm.ClearCacheSwappableTests.test_clear_cache_clears_multiple_keys apps.tests_llm.ClearCacheSwappableTests.test_clear_cache_does_not_corrupt_other_registry apps.tests_llm.ClearCacheSwappableTests.test_clear_cache_idempotent apps.tests_llm.ClearCacheSwappableTests.test_clear_cache_preserves_behavior_afterwards apps.tests_llm.ClearCacheSwappableTests.test_clear_cache_thread_safety apps.tests_llm.ClearCacheSwappableTests.test_clear_cache_when_not_ready apps.tests_llm.ClearCacheSwappableTests.test_get_swappable_recomputed_after_clear
coverage json -o coverage.json
: '>>>>> End Test Output'
