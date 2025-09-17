#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 apps.tests_llm.SwappableCacheTests.tearDown apps.tests_llm.SwappableCacheTests.test_clear_cache_case_insensitive_key_cleared apps.tests_llm.SwappableCacheTests.test_clear_cache_multiple_times_clears_cache apps.tests_llm.SwappableCacheTests.test_clear_cache_no_swappable_model_results_in_empty_cache_after_clear apps.tests_llm.SwappableCacheTests.test_clear_cache_on_new_registry_clears_cache apps.tests_llm.SwappableCacheTests.test_get_swappable_settings_name_cache_info_exists_and_cleared apps.tests_llm.SwappableCacheTests.test_isolated_registry_get_models_after_swappable_cleared apps.tests_llm.SwappableCacheTests.test_isolated_registry_swappable_after_get_models_cleared apps.tests_llm.SwappableCacheTests.test_isolated_registry_swapped_model_cache_cleared apps.tests_llm.SwappableCacheTests.test_main_registry_swappable_cache_cleared apps.tests_llm.SwappableCacheTests.test_swappable_cache_recomputes_after_clear
coverage json -o coverage.json
: '>>>>> End Test Output'
