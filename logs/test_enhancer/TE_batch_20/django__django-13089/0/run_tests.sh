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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 cache.tests_llm.DBCacheCullTests._call_cull cache.tests_llm.DBCacheCullTests.create_table cache.tests_llm.DBCacheCullTests.drop_table cache.tests_llm.DBCacheCullTests.setUp cache.tests_llm.DBCacheCullTests.tearDown cache.tests_llm.DBCacheCullTests.test_cull_clear_called_when_frequency_zero cache.tests_llm.DBCacheCullTests.test_cull_deletes_with_last_cache_key cache.tests_llm.DBCacheCullTests.test_cull_executes_cull_sql_with_zero_cull_num cache.tests_llm.DBCacheCullTests.test_cull_handles_no_last_cache_key cache.tests_llm.DBCacheCullTests.test_cull_no_action_when_count_not_exceed_max cache.tests_llm.DBCacheCullTests.test_cull_with_empty_string_last_key cache.tests_llm.DBCacheCullTests.test_cull_with_none_in_last_key_tuple cache.tests_llm.DBCacheCullTests.test_multiple_cull_invocations_do_not_crash cache.tests_llm.execs'] (cache.tests_llm.DBCacheCullTests.['DummyCursor.__init__', 'DummyCursor.execute', 'DummyCursor.fetchone', 'DummyCursor.__enter__', 'DummyCursor.__exit__', 'DummyCursor)
coverage json -o coverage.json
: '>>>>> End Test Output'
