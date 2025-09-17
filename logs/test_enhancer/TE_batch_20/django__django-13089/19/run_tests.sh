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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 cache.tests_llm.CullQueryNoneReturnTests._force_zero_cull_conditions cache.tests_llm.CullQueryNoneReturnTests._restore_cull_settings cache.tests_llm.CullQueryNoneReturnTests.setUp cache.tests_llm.CullQueryNoneReturnTests.tearDown cache.tests_llm.CullQueryNoneReturnTests.test_add_does_not_crash_when_cull_query_returns_no_rows cache.tests_llm.CullQueryNoneReturnTests.test_cull_frequency_zero_calls_clear_and_works cache.tests_llm.CullQueryNoneReturnTests.test_expired_rows_removed_and_no_crash_when_cull_query_returns_no_rows cache.tests_llm.CullQueryNoneReturnTests.test_multiple_operations_do_not_crash_under_zero_cull_num cache.tests_llm.CullQueryNoneReturnTests.test_no_unexpected_deletion_happens_when_cull_query_returns_no_rows cache.tests_llm.CullQueryNoneReturnTests.test_set_does_not_crash_when_cull_query_returns_no_rows_multiple cache.tests_llm.CullQueryNoneReturnTests.test_set_does_not_crash_when_cull_query_returns_no_rows_single cache.tests_llm.CullQueryNoneReturnTests.test_set_many_does_not_crash_when_cull_query_returns_no_rows cache.tests_llm.CullQueryNoneReturnTests.test_touch_does_not_crash_when_cull_query_returns_no_rows
coverage json -o coverage.json
: '>>>>> End Test Output'
