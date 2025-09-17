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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 cache.tests_llm.AdditionalDBCullTests._db_for_cache cache.tests_llm.AdditionalDBCullTests._row_count cache.tests_llm.AdditionalDBCullTests.setUp cache.tests_llm.AdditionalDBCullTests.tearDown cache.tests_llm.AdditionalDBCullTests.test_base_delete_many_empty_returns_false cache.tests_llm.AdditionalDBCullTests.test_create_and_drop_cache_table_commands_work cache.tests_llm.AdditionalDBCullTests.test_cull_respects_max_entries cache.tests_llm.AdditionalDBCullTests.test_delete_many_removes_keys cache.tests_llm.AdditionalDBCullTests.test_multiple_cull_calls_do_not_crash cache.tests_llm.AdditionalDBCullTests.test_set_triggers_cull_when_num_exceeds_max_entries
coverage json -o coverage.json
: '>>>>> End Test Output'
