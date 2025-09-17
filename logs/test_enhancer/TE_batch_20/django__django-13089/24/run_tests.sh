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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 cache.tests_llm.DBCullRegressionTests.setUp cache.tests_llm.DBCullRegressionTests.tearDown cache.tests_llm.DBCullRegressionTests.test_cull_deletes_when_last_cache_key_present cache.tests_llm.DBCullRegressionTests.test_cull_deletion_sql_parameter_is_used cache.tests_llm.DBCullRegressionTests.test_cull_handles_no_last_cache_key_tuple_with_none cache.tests_llm.__exit__'] (cache.tests_llm.DBCullRegressionTests.['DummyCursor.__init__', 'DummyCursor.execute', 'DummyCursor.fetchone', 'DummyCursor.__enter__', 'DummyCursor)
coverage json -o coverage.json
: '>>>>> End Test Output'
