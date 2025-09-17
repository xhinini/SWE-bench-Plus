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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 cache.tests_llm.DatabaseCacheCullFetchoneNoneTests.setUp cache.tests_llm.DatabaseCacheCullFetchoneNoneTests.tearDown cache.tests_llm.DatabaseCacheCullFetchoneNoneTests.test_set_returns_true_even_when_cull_select_returns_no_rows cache.tests_llm.DatabaseCacheCullFetchoneNoneTests.test_set_two_keys_triggers_cull_but_does_not_raise
coverage json -o coverage.json
: '>>>>> End Test Output'
