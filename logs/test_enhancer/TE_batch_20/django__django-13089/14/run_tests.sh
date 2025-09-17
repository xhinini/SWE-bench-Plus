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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 cache.tests_llm.DBCacheCullingTests._get_db cache.tests_llm.DBCacheCullingTests.setUp cache.tests_llm.DBCacheCullingTests.test_cull_computes_cull_num_and_calls_culling_sql_with_cull_num cache.tests_llm.DBCacheCullingTests.test_cull_with_last_cache_key_bytes_executes_delete_with_decoded_bytes cache.tests_llm.DBCacheCullingTests.test_cull_with_last_cache_key_executes_delete_with_key
coverage json -o coverage.json
: '>>>>> End Test Output'
