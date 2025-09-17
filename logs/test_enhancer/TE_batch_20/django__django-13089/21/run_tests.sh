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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 cache.tests_llm.DBCacheCullingRegressionTests._patch_default_cursor cache.tests_llm.DBCacheCullingRegressionTests._restore_default_cursor cache.tests_llm.DBCacheCullingRegressionTests.setUp cache.tests_llm.DBCacheCullingRegressionTests.tearDown cache.tests_llm.DBCacheCullingRegressionTests.test_add_does_not_crash_when_no_last_cache_key cache.tests_llm.DBCacheCullingRegressionTests.test_cull_calls_clear_when_cull_frequency_zero cache.tests_llm.DBCacheCullingRegressionTests.test_cull_no_last_cache_key_does_not_execute_final_delete cache.tests_llm.DBCacheCullingRegressionTests.test_cull_with_last_cache_key_executes_final_delete cache.tests_llm.DBCacheCullingRegressionTests.test_final_delete_parameter_matches_last_cache_key cache.tests_llm.DBCacheCullingRegressionTests.test_no_cull_when_num_leq_max_entries cache.tests_llm.DBCacheCullingRegressionTests.test_repeated_sets_do_not_crash_when_no_last_cache_key cache.tests_llm.DBCacheCullingRegressionTests.test_set_returns_true_when_no_last_cache_key cache.tests_llm.DBCacheCullingRegressionTests.test_touch_handles_no_last_cache_key_gracefully
coverage json -o coverage.json
: '>>>>> End Test Output'
