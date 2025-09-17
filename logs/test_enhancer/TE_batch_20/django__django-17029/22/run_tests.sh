#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 apps.tests_llm.ClearCacheOrderTests._patch_clears apps.tests_llm.ClearCacheOrderTests.setUp apps.tests_llm.ClearCacheOrderTests.test_clear_cache_called_when_ready_false_and_apps_present apps.tests_llm.ClearCacheOrderTests.test_clear_cache_multiple_models_ordering apps.tests_llm.ClearCacheOrderTests.test_clear_cache_no_app_configs_does_not_expire apps.tests_llm.ClearCacheOrderTests.test_expire_exception_propagated_after_clears apps.tests_llm.ClearCacheOrderTests.test_get_models_exception_swappable_cleared_first apps.tests_llm.ClearCacheOrderTests.test_order_with_multiple_apps_models apps.tests_llm.ClearCacheOrderTests.test_order_with_one_app_one_model apps.tests_llm.ClearCacheOrderTests.test_swappable_before_get_models_ready_false apps.tests_llm.ClearCacheOrderTests.test_swappable_before_get_models_ready_true_no_apps apps.tests_llm.ClearCacheOrderTests.test_swappable_exception_prevents_get_models_called apps.tests_llm.DummyAppConfig.__init__ apps.tests_llm.DummyAppConfig.get_models apps.tests_llm.DummyModel.__init__
coverage json -o coverage.json
: '>>>>> End Test Output'
