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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 cache.tests_llm.CullFetchoneNoneTests._configure_cache_for_zero_cull cache.tests_llm.CullFetchoneNoneTests.setUp cache.tests_llm.CullFetchoneNoneTests.tearDown cache.tests_llm.CullFetchoneNoneTests.test_add_triggers_cull_with_cull_num_zero cache.tests_llm.CullFetchoneNoneTests.test_prefixed_cache_cull_num_zero cache.tests_llm.CullFetchoneNoneTests.test_preserve_entries_when_cull_num_zero cache.tests_llm.CullFetchoneNoneTests.test_repeated_operations_do_not_raise_on_cull_num_zero cache.tests_llm.CullFetchoneNoneTests.test_set_many_triggers_cull_with_cull_num_zero cache.tests_llm.CullFetchoneNoneTests.test_set_triggers_cull_with_cull_num_zero cache.tests_llm.CullFetchoneNoneTests.test_touch_triggers_cull_with_cull_num_zero cache.tests_llm.CullFetchoneNoneTests.test_unicode_keys_cull_num_zero cache.tests_llm.CullFetchoneNoneTests.test_versioned_keys_cull_num_zero
coverage json -o coverage.json
: '>>>>> End Test Output'
