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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 cache.tests_llm.CullRegressionTests._patch_cursor_to_return_no_last_row cache.tests_llm.CullRegressionTests.create_table cache.tests_llm.CullRegressionTests.drop_table cache.tests_llm.CullRegressionTests.setUp cache.tests_llm.CullRegressionTests.tearDown cache.tests_llm.CullRegressionTests.test_cull_does_not_delete_when_no_last_key cache.tests_llm.CullRegressionTests.test_cull_interaction_with_expired_rows_and_none_last_row cache.tests_llm.CullRegressionTests.test_cull_with_cull_frequency_one_and_no_last_row cache.tests_llm.CullRegressionTests.test_cull_with_large_cull_num_returns_none_handled cache.tests_llm.CullRegressionTests.test_cull_with_mixed_timeouts_and_none_last_row cache.tests_llm.CullRegressionTests.test_cull_with_zero_cull_frequency_no_exception cache.tests_llm.CullRegressionTests.test_direct_cull_call_handles_none_last_cache_key cache.tests_llm.CullRegressionTests.test_multiple_cull_attempts_with_no_last_row_are_safe cache.tests_llm.CullRegressionTests.test_set_triggers_cull_without_last_cache_key
coverage json -o coverage.json
: '>>>>> End Test Output'
