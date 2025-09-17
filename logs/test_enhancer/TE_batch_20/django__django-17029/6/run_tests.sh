#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 apps.tests_llm.ClearCacheRegressionTests.tearDown apps.tests_llm.ClearCacheRegressionTests.test_clear_cache_after_manual_cache_population apps.tests_llm.ClearCacheRegressionTests.test_clear_cache_after_set_available_apps apps.tests_llm.ClearCacheRegressionTests.test_clear_cache_after_unset_available_apps_restores_state apps.tests_llm.ClearCacheRegressionTests.test_clear_cache_clears_swappable_cache_simple apps.tests_llm.ClearCacheRegressionTests.test_clear_cache_does_not_affect_other_registries apps.tests_llm.ClearCacheRegressionTests.test_clear_cache_does_not_raise_when_called_repeatedly apps.tests_llm.ClearCacheRegressionTests.test_clear_cache_in_isolated_registry apps.tests_llm.ClearCacheRegressionTests.test_clear_cache_multiple_calls_no_side_effects apps.tests_llm.ClearCacheRegressionTests.test_clear_cache_on_new_registry_instance
coverage json -o coverage.json
: '>>>>> End Test Output'
