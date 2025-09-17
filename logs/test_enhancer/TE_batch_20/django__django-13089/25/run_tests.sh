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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 cache.tests_llm.DBCacheCullingRegressionTests._force_cull_configuration cache.tests_llm.DBCacheCullingRegressionTests._restore_cull_configuration cache.tests_llm.DBCacheCullingRegressionTests.setUp cache.tests_llm.DBCacheCullingRegressionTests.tearDown cache.tests_llm.DBCacheCullingRegressionTests.test_add_does_not_crash_when_culling_fetchone_returns_none cache.tests_llm.DBCacheCullingRegressionTests.test_multiple_sets_do_not_crash_when_culling_fetchone_returns_none cache.tests_llm.DBCacheCullingRegressionTests.test_overwrite_does_not_crash_when_culling_fetchone_returns_none cache.tests_llm.DBCacheCullingRegressionTests.test_set_does_not_crash_when_culling_fetchone_returns_none cache.tests_llm.DBCacheCullingRegressionTests.test_set_many_does_not_crash_when_culling_fetchone_returns_none cache.tests_llm.DBCacheCullingRegressionTests.test_set_then_add_does_not_crash_when_culling_fetchone_returns_none cache.tests_llm.DBCacheCullingRegressionTests.test_set_with_expired_entries_does_not_crash_when_culling_fetchone_returns_none cache.tests_llm.DBCacheCullingRegressionTests.test_touch_does_not_crash_when_culling_fetchone_returns_none cache.tests_llm.DBCacheCullingRegressionTests.test_touch_nonexistent_does_not_crash_when_culling_fetchone_returns_none
coverage json -o coverage.json
: '>>>>> End Test Output'
