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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 bulk_create.tests_llm.test_batch_size_none_uses_max_batch_size bulk_create.tests_llm.test_batch_size_smaller_than_max_uses_provided_batch_size bulk_create.tests_llm.test_batched_insert_min_batch_size_at_least_one bulk_create.tests_llm.test_bulk_create_respects_max_with_mixed_returning bulk_create.tests_llm.test_can_return_rows_bulk_create_respects_max bulk_create.tests_llm.test_explicit_batch_size_respects_max_batch_size_country_variant bulk_create.tests_llm.test_explicit_batch_size_respects_max_batch_size_twofields bulk_create.tests_llm.test_ignore_conflicts_respects_max bulk_create.tests_llm.test_mixed_pks_respects_max_batch_size
coverage json -o coverage.json
: '>>>>> End Test Output'
