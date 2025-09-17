#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 apps.tests_llm.ClearCacheSwappableTests.assert_swappable_cache_cleared_after_clear apps.tests_llm.ClearCacheSwappableTests.make_registry apps.tests_llm.ClearCacheSwappableTests.test_clear_cache_clears_multiple_cached_keys apps.tests_llm.ClearCacheSwappableTests.test_clear_cache_when_registry_not_ready apps.tests_llm.ClearCacheSwappableTests.test_clear_cache_with_prepopulated_models_cache apps.tests_llm.ClearCacheSwappableTests.test_many_models_repopping apps.tests_llm.ClearCacheSwappableTests.test_multiple_appconfigs_expire_and_touch_cache apps.tests_llm.ClearCacheSwappableTests.test_multiple_models_different_keys apps.tests_llm.ClearCacheSwappableTests.test_multiple_models_same_key apps.tests_llm.ClearCacheSwappableTests.test_single_model_swappable_label_match apps.tests_llm.ClearCacheSwappableTests.test_single_model_swapped_attribute apps.tests_llm.FakeAppConfig.__init__ apps.tests_llm.FakeAppConfig.get_models apps.tests_llm.FakeMeta.__init__ apps.tests_llm.FakeMeta._expire_cache apps.tests_llm.FakeModel.__init__
coverage json -o coverage.json
: '>>>>> End Test Output'
