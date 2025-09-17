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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 cache.tests_llm.DBCullEdgeCaseTests._run_cull_with_responses cache.tests_llm.DBCullEdgeCaseTests.setUp cache.tests_llm.DBCullEdgeCaseTests.test_cull_clear_called_when_cull_frequency_zero cache.tests_llm.DBCullEdgeCaseTests.test_cull_deletes_when_last_cache_key_list cache.tests_llm.DBCullEdgeCaseTests.test_cull_deletes_when_last_cache_key_tuple cache.tests_llm.DBCullEdgeCaseTests.test_cull_handles_last_cache_key_empty_list cache.tests_llm.DBCullEdgeCaseTests.test_cull_handles_last_cache_key_empty_tuple cache.tests_llm.DBCullEdgeCaseTests.test_cull_handles_last_cache_key_none cache.tests_llm.DBCullEdgeCaseTests.test_cull_handles_last_cache_key_tuple_with_empty_string_inside cache.tests_llm.DBCullEdgeCaseTests.test_cull_handles_multiple_consecutive_calls_with_none cache.tests_llm.DBCullEdgeCaseTests.test_cull_no_delete_when_cull_num_zero_and_no_last_key cache.tests_llm.DBCullEdgeCaseTests.test_cull_robust_with_unexpected_fetchone_types cache.tests_llm.DummyCursor.__init__ cache.tests_llm.DummyCursor.execute cache.tests_llm.DummyCursor.fetchall cache.tests_llm.DummyCursor.fetchone
coverage json -o coverage.json
: '>>>>> End Test Output'
