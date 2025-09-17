#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 apps.tests_llm.ClearCacheOrderTests._patch_cache_clear_methods apps.tests_llm.ClearCacheOrderTests._restore_cache_clear_methods apps.tests_llm.ClearCacheOrderTests.test_clear_cache_called_twice_preserves_order apps.tests_llm.ClearCacheOrderTests.test_clear_cache_order_after_populating_caches apps.tests_llm.ClearCacheOrderTests.test_clear_cache_order_for_multiple_registries apps.tests_llm.ClearCacheOrderTests.test_clear_cache_order_main_registry_not_ready apps.tests_llm.ClearCacheOrderTests.test_clear_cache_order_main_registry_ready apps.tests_llm.ClearCacheOrderTests.test_clear_cache_order_new_registry_not_ready apps.tests_llm.ClearCacheOrderTests.test_clear_cache_order_new_registry_ready apps.tests_llm.ClearCacheOrderTests.test_clear_cache_order_on_isolated_registry apps.tests_llm.ClearCacheOrderTests.test_clear_cache_order_with_nonempty_app_configs apps.tests_llm.ClearCacheOrderTests.test_clear_cache_order_with_ready_toggle
coverage json -o coverage.json
: '>>>>> End Test Output'
