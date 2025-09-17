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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 cache.tests_llm.CullRegressionTests._count_table_rows cache.tests_llm.CullRegressionTests.setUp cache.tests_llm.CullRegressionTests.tearDown cache.tests_llm.CullRegressionTests.test_base_set_triggers_cull_and_handles_no_last_cache_key cache.tests_llm.CullRegressionTests.test_cull_handles_no_last_cache_key_multiple_rows cache.tests_llm.CullRegressionTests.test_cull_handles_no_last_cache_key_single_row cache.tests_llm.CullRegressionTests.test_cull_handles_no_last_cache_key_with_expired_rows cache.tests_llm.CullRegressionTests.test_cull_no_last_cache_key_does_not_clear_when_frequency_nonzero cache.tests_llm.CullRegressionTests.test_cull_no_last_cache_key_timezone_aware cache.tests_llm.CullRegressionTests.test_cull_no_last_cache_key_timezone_naive cache.tests_llm.CullRegressionTests.test_cull_with_cull_frequency_one_and_no_last_cache_key cache.tests_llm.CullRegressionTests.test_cull_with_many_rows_and_no_last_cache_key_preserves_rows
coverage json -o coverage.json
: '>>>>> End Test Output'
