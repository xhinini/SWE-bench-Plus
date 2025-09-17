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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 cache.tests_llm.FakeCursor.__init__ cache.tests_llm.FakeCursor.execute cache.tests_llm.FakeCursor.fetchone cache.tests_llm._get_table_for_default_cache cache.tests_llm.test_cull_calls_clear_when_cull_frequency_zero cache.tests_llm.test_cull_does_not_execute_delete_when_no_last_cache_key cache.tests_llm.test_cull_executes_culling_sql_with_cull_num_and_handles_no_result cache.tests_llm.test_cull_executes_delete_when_last_cache_key_present cache.tests_llm.test_cull_handles_none_last_cache_key_no_exception cache.tests_llm.test_cull_multiple_times_with_none_last_key cache.tests_llm.test_cull_none_last_key_when_adapter_used cache.tests_llm.test_cull_skips_culling_when_num_below_max_entries cache.tests_llm.test_cull_with_empty_string_key_performs_delete cache.tests_llm.test_repeated_cull_varied_counts
coverage json -o coverage.json
: '>>>>> End Test Output'
