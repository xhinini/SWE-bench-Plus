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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 bulk_create.tests_llm.test_respect_max_batch_size_country_extra bulk_create.tests_llm.test_respect_max_batch_size_exactly_one_over_triggers_cap bulk_create.tests_llm.test_respect_max_batch_size_large_overage bulk_create.tests_llm.test_respect_max_batch_size_mixed_pk bulk_create.tests_llm.test_respect_max_batch_size_multiple_small_calls bulk_create.tests_llm.test_respect_max_batch_size_restaurant bulk_create.tests_llm.test_respect_max_batch_size_twofields bulk_create.tests_llm.test_respect_max_batch_size_with_ignore_conflicts bulk_create.tests_llm.test_respect_max_batch_size_with_returning
coverage json -o coverage.json
: '>>>>> End Test Output'
