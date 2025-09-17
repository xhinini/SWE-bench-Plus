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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 cache.tests_llm.DatabaseCacheCullUnitTests._make_cursor cache.tests_llm.DatabaseCacheCullUnitTests.setUp cache.tests_llm.DatabaseCacheCullUnitTests.test_cull_uses_computed_cull_num cache.tests_llm.DatabaseCacheCullUnitTests.test_cull_uses_connection_for_table_quoting cache.tests_llm.DatabaseCacheCullUnitTests.test_final_delete_executes_when_last_cache_key_returned cache.tests_llm.DatabaseCacheCullUnitTests.test_no_cull_when_num_less_than_or_equal_max_entries
coverage json -o coverage.json
: '>>>>> End Test Output'
