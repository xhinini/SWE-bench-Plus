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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 cache.tests_llm.CullRegressionTests._now cache.tests_llm.CullRegressionTests.setUp cache.tests_llm.CullRegressionTests.tearDown cache.tests_llm.CullRegressionTests.test_cull_delete_uses_quoted_table_name cache.tests_llm.CullRegressionTests.test_cull_executes_delete_when_last_cache_key_present cache.tests_llm.CullRegressionTests.test_cull_handles_empty_tuple_from_fetchone cache.tests_llm.CullRegressionTests.test_cull_handles_multiple_none_fetchone_calls_gracefully cache.tests_llm.CullRegressionTests.test_cull_handles_no_last_cache_key cache.tests_llm.CullRegressionTests.test_cull_noop_when_count_not_exceeding_max cache.tests_llm.CullRegressionTests.test_cull_with_zero_length_string_key_deletes cache.tests_llm.CullRegressionTests.test_expired_rows_delete_passes_adapted_datetime_value cache.tests_llm.fetchone'] (cache.tests_llm.CullRegressionTests.['_FakeCursor.__init__', '_FakeCursor.execute', '_FakeCursor)
coverage json -o coverage.json
: '>>>>> End Test Output'
