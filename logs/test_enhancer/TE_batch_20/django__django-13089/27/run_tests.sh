#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
sed -i '/en_US.UTF-8/s/^# //g' /etc/locale.gen && locale-gen
export LANG=en_US.UTF-8
export LANGUAGE=en_US:en
export LC_ALL=en_US.UTF-8
export PYTHONIOENCODING=utf8
python --version && python -m pip install -U pip
python -m pip install -U 'coverage==6.2'

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 cache.tests_llm.DBCacheCullingRegressionTests.test_byte_last_cache_key_is_accepted_and_used_in_delete cache.tests_llm.DBCacheCullingRegressionTests.test_cull_does_not_crash_on_add_even_if_culling_select_returns_none cache.tests_llm.DBCacheCullingRegressionTests.test_cull_does_not_crash_when_last_cache_key_fetchone_is_none_on_add cache.tests_llm.DBCacheCullingRegressionTests.test_cull_does_not_crash_when_last_cache_key_fetchone_is_none_on_set cache.tests_llm.DBCacheCullingRegressionTests.test_cull_does_not_crash_when_last_cache_key_fetchone_is_none_on_touch cache.tests_llm.DBCacheCullingRegressionTests.test_cull_with_multiple_consecutive_calls_does_not_error cache.tests_llm.DBCacheCullingRegressionTests.test_delete_attempted_when_last_cache_key_present cache.tests_llm.DBCacheCullingRegressionTests.test_direct_cull_call_handles_none_last_cache_key cache.tests_llm.DBCacheCullingRegressionTests.test_no_delete_attempted_when_last_cache_key_is_none cache.tests_llm.DBCacheCullingRegressionTests.test_zero_cull_frequency_does_not_crash cache.tests_llm.FakeCursor.__enter__ cache.tests_llm.FakeCursor.__exit__ cache.tests_llm.FakeCursor.__init__ cache.tests_llm.FakeCursor.execute cache.tests_llm.FakeCursor.fetchone
coverage json -o coverage.json
: '>>>>> End Test Output'
