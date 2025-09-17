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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 bulk_create.tests_llm.test__batched_insert_batch_size_equal_to_max bulk_create.tests_llm.test__batched_insert_batch_size_greater_than_max_is_capped bulk_create.tests_llm.test__batched_insert_batch_size_less_than_max_kept bulk_create.tests_llm.test__batched_insert_batch_size_none_uses_max bulk_create.tests_llm.test__batched_insert_collects_inserted_rows_when_bulk_return_list bulk_create.tests_llm.test__batched_insert_collects_inserted_rows_when_bulk_return_single bulk_create.tests_llm.test__batched_insert_does_not_collect_when_bulk_return_false bulk_create.tests_llm.test__batched_insert_many_batches_with_large_count_and_capping bulk_create.tests_llm.test__batched_insert_minimum_batch_size_one_when_ops_returns_zero bulk_create.tests_llm.test__batched_insert_raises_when_ignore_conflicts_unsupported
coverage json -o coverage.json
: '>>>>> End Test Output'
