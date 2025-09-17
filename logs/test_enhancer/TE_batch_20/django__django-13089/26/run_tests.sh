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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 cache.tests_llm.TinyCullDBTests.setUp cache.tests_llm.TinyCullDBTests.tearDown cache.tests_llm.TinyCullDBTests.test_add_after_delete_no_crash cache.tests_llm.TinyCullDBTests.test_add_no_crash cache.tests_llm.TinyCullDBTests.test_binary_values_culling_no_crash cache.tests_llm.TinyCullDBTests.test_multiple_rapid_sets_no_crash cache.tests_llm.TinyCullDBTests.test_set_after_expiry_removes_expired cache.tests_llm.TinyCullDBTests.test_set_many_no_crash cache.tests_llm.TinyCullDBTests.test_set_many_with_mixed_timeouts_no_crash cache.tests_llm.TinyCullDBTests.test_set_two_keys_no_crash cache.tests_llm.TinyCullDBTests.test_touch_no_crash cache.tests_llm.TinyCullDBTests.test_touch_nonexistent_returns_false_and_no_crash
coverage json -o coverage.json
: '>>>>> End Test Output'
