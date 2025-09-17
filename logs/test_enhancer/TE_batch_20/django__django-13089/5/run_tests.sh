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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 cache.tests_llm.DBCullRegressionTests._now cache.tests_llm.DBCullRegressionTests.setUp cache.tests_llm.DBCullRegressionTests.tearDown cache.tests_llm.DBCullRegressionTests.test_cull_calls_clear_when_cull_frequency_zero cache.tests_llm.DBCullRegressionTests.test_cull_does_nothing_if_num_not_exceed_max_entries cache.tests_llm.DBCullRegressionTests.test_cull_handles_last_cache_key_none_tuple cache.tests_llm.DBCullRegressionTests.test_cull_no_last_cache_key_does_not_execute_delete cache.tests_llm.DBCullRegressionTests.test_cull_no_last_cache_key_does_not_raise cache.tests_llm.DBCullRegressionTests.test_cull_uses_adapt_datetimefield_value_on_delete cache.tests_llm.DBCullRegressionTests.test_cull_uses_cache_key_culling_sql_with_cull_num cache.tests_llm.DBCullRegressionTests.test_cull_with_last_cache_key_executes_delete_with_key cache.tests_llm.DBCullRegressionTests.test_multiple_cull_calls_with_varied_fetchone_sequences cache.tests_llm.fetchone'] (cache.tests_llm.DBCullRegressionTests.['FakeCursor.__init__', 'FakeCursor.execute', 'FakeCursor)
coverage json -o coverage.json
: '>>>>> End Test Output'
