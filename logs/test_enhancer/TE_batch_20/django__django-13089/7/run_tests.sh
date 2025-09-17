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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 cache.tests_llm.DBCullRegressionTests.setUp cache.tests_llm.DBCullRegressionTests.tearDown cache.tests_llm.DBCullRegressionTests.test_cull_multiple_calls_consistent cache.tests_llm.DBCullRegressionTests.test_cull_with_last_cache_key_executes_delete cache.tests_llm.fetchone'] (cache.tests_llm.DBCullRegressionTests.['FakeCursor.__init__', 'FakeCursor.execute', 'FakeCursor)
coverage json -o coverage.json
: '>>>>> End Test Output'
