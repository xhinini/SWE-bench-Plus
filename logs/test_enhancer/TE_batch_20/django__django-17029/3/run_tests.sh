#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 apps.tests_llm.ClearCacheSwappableTests._run_scenario_and_assert_cache_cleared apps.tests_llm.ClearCacheSwappableTests.setUp apps.tests_llm.ClearCacheSwappableTests.tearDown apps.tests_llm.ClearCacheSwappableTests.test_clear_cache_idempotence_when_called_multiple_times apps.tests_llm.ClearCacheSwappableTests.test_clear_cache_repopulated_with_different_keys apps.tests_llm.ClearCacheSwappableTests.test_clear_cache_when_not_ready_does_not_run_expire_but_clears_cache apps.tests_llm.ClearCacheSwappableTests.test_clear_cache_with_many_repopulations apps.tests_llm.ClearCacheSwappableTests.test_clear_cache_with_mixed_behaviors apps.tests_llm.ClearCacheSwappableTests.test_expire_does_not_call_swappable_but_cache_still_cleared apps.tests_llm.ClearCacheSwappableTests.test_multiple_apps_each_with_models_that_expire apps.tests_llm.ClearCacheSwappableTests.test_single_model_expire_repopulates_swappable_cache apps.tests_llm.ClearCacheSwappableTests.test_two_models_in_one_app_each_expire apps.tests_llm.FakeAppConfig.__init__ apps.tests_llm.FakeAppConfig.get_models apps.tests_llm.FakeMeta.__init__ apps.tests_llm.FakeMeta._expire_cache apps.tests_llm.FakeModel.__init__ apps.tests_llm.FakeModel.__repr__
coverage json -o coverage.json
: '>>>>> End Test Output'
