#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 apps.tests_llm.ClearCacheTests.test_clear_cache_does_not_raise_when_models_ready_false_but_models_cache_empty apps.tests_llm.ClearCacheTests.test_clear_cache_during_expire_cache_does_not_leave_swappable_cache_populated apps.tests_llm.ClearCacheTests.test_clear_cache_for_main_registry_with_fake_expire_repopulation apps.tests_llm.ClearCacheTests.test_clear_cache_when_appconfigs_empty_only_clears_caches apps.tests_llm.ClearCacheTests.test_clear_cache_when_not_ready_still_clears_swappable_and_models apps.tests_llm.ClearCacheTests.test_clear_cache_with_multiple_models_and_expire_repopulation apps.tests_llm.ClearCacheTests.test_custom_apps_clear_cache_clears_both_caches apps.tests_llm.ClearCacheTests.test_main_registry_clear_cache_clears_both_caches apps.tests_llm.ClearCacheTests.test_multiple_clear_cache_calls_idempotent apps.tests_llm.FakeModel.__init__ apps.tests_llm.MetaStub.__init__ apps.tests_llm.MetaStub._expire_cache apps.tests_llm.StubAppConfig.__init__ apps.tests_llm.StubAppConfig.get_models
coverage json -o coverage.json
: '>>>>> End Test Output'
