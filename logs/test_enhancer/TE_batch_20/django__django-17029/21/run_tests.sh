#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 apps.tests_llm.ClearCacheOrderTests.test_clear_cache_call_order_main_registry_not_ready apps.tests_llm.ClearCacheOrderTests.test_clear_cache_call_order_main_registry_ready apps.tests_llm.ClearCacheOrderTests.test_clear_cache_call_order_new_apps_not_ready apps.tests_llm.ClearCacheOrderTests.test_clear_cache_call_order_new_apps_ready apps.tests_llm.ClearCacheOrderTests.test_clear_cache_call_order_via_set_available_apps apps.tests_llm.ClearCacheOrderTests.test_clear_cache_call_order_via_unset_available_apps apps.tests_llm.ClearCacheOrderTests.test_clear_cache_call_order_via_unset_installed_apps apps.tests_llm.ClearCacheOrderTests.test_clear_cache_multiple_consecutive_calls_preserve_order apps.tests_llm.ClearCacheOrderTests.test_clear_cache_only_invokes_expected_cache_clears apps.tests_llm.ClearCacheOrderTests.test_clear_cache_order_on_custom_apps_instance_after_state_change apps.tests_llm._patch_cache_clears
coverage json -o coverage.json
: '>>>>> End Test Output'
