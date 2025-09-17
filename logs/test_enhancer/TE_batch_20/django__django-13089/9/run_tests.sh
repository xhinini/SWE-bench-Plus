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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 cache.tests_llm.CullingEmptyResultTests._patch_cull_sql_and_force_cull cache.tests_llm.CullingEmptyResultTests.setUp cache.tests_llm.CullingEmptyResultTests.tearDown cache.tests_llm.CullingEmptyResultTests.test_add_after_expired_entry_handles_empty_cull_result cache.tests_llm.CullingEmptyResultTests.test_add_handles_empty_cull_result cache.tests_llm.CullingEmptyResultTests.test_multiple_consecutive_sets_handle_empty_cull_result cache.tests_llm.CullingEmptyResultTests.test_set_does_not_delete_other_key_when_cull_result_empty cache.tests_llm.CullingEmptyResultTests.test_set_handles_empty_cull_result cache.tests_llm.CullingEmptyResultTests.test_set_many_handles_empty_cull_result cache.tests_llm.CullingEmptyResultTests.test_set_many_then_get_handles_empty_cull_result cache.tests_llm.CullingEmptyResultTests.test_set_then_touch_handles_empty_cull_result cache.tests_llm.CullingEmptyResultTests.test_touch_handles_empty_cull_result cache.tests_llm.CullingEmptyResultTests.test_touch_nonexistent_handles_empty_cull_result
coverage json -o coverage.json
: '>>>>> End Test Output'
