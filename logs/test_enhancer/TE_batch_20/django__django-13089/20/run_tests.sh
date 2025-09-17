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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 cache.tests_llm.test__cull_calls_clear_when_cull_frequency_zero cache.tests_llm.test__cull_deletes_when_last_cache_key_present cache.tests_llm.test__cull_handles_last_cache_key_as_bytes cache.tests_llm.test__cull_handles_last_cache_key_with_none_element cache.tests_llm.test__cull_handles_none_last_cache_key_no_delete cache.tests_llm.test__cull_multiple_execute_calls_observed cache.tests_llm.test__cull_no_culling_if_count_not_exceeding_max_entries cache.tests_llm.test__cull_no_exception_when_cull_num_is_zero_and_no_last_key cache.tests_llm.test__cull_passes_computed_cull_num_to_culling_sql
coverage json -o coverage.json
: '>>>>> End Test Output'
