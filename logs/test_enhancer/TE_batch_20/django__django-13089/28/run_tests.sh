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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 cache.tests_llm.DBCullRegressionTests._row_count cache.tests_llm.DBCullRegressionTests.setUp cache.tests_llm.DBCullRegressionTests.tearDown cache.tests_llm.DBCullRegressionTests.test_cull_deletes_keys_up_to_last_cache_key cache.tests_llm.DBCullRegressionTests.test_cull_does_not_raise_on_empty_table cache.tests_llm.DBCullRegressionTests.test_cull_does_nothing_when_not_over_max cache.tests_llm.DBCullRegressionTests.test_cull_handles_fetchone_none_during_culling cache.tests_llm.DBCullRegressionTests.test_cull_handles_fetchone_returning_none_via_monkeypatch cache.tests_llm.DBCullRegressionTests.test_cull_handles_non_ascii_keys cache.tests_llm.DBCullRegressionTests.test_cull_reduces_count_consistently_on_repeated_triggers cache.tests_llm.DBCullRegressionTests.test_cull_with_cull_frequency_zero_calls_clear cache.tests_llm.DBCullRegressionTests.test_multiple_cull_calls_are_idempotent
coverage json -o coverage.json
: '>>>>> End Test Output'
