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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 cache.tests_llm.DatabaseCacheCullTests.make_connection cache.tests_llm.DatabaseCacheCullTests.test_cull_executes_culling_sql_with_correct_cull_num cache.tests_llm.DatabaseCacheCullTests.test_cull_uses_adapt_datetimefield_value_for_expires_delete cache.tests_llm.DatabaseCacheCullTests.test_cull_uses_quote_name_in_table_references cache.tests_llm.DatabaseCacheCullTests.test_cull_with_last_key_executes_final_delete_with_key cache.tests_llm.DatabaseCacheCullTests.test_final_delete_passes_bytes_key_unchanged cache.tests_llm.DatabaseCacheCullTests.test_sequence_of_execute_calls_when_culling_happens
coverage json -o coverage.json
: '>>>>> End Test Output'
