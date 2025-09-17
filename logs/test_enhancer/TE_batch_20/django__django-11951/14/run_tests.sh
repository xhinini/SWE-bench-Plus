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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 bulk_create.tests_llm.BatchedInsertBatchingTests.make_objs bulk_create.tests_llm.BatchedInsertBatchingTests.test_batch_size_capped_to_max_when_larger bulk_create.tests_llm.BatchedInsertBatchingTests.test_batch_size_equal_to_max bulk_create.tests_llm.BatchedInsertBatchingTests.test_batch_size_none_uses_max_batch_size bulk_create.tests_llm.BatchedInsertBatchingTests.test_batch_size_used_when_smaller_than_max bulk_create.tests_llm.BatchedInsertBatchingTests.test_batched_insert_raises_on_unsupported_ignore_conflicts bulk_create.tests_llm.BatchedInsertBatchingTests.test_bulk_create_forwards_ignore_conflicts_flag_to_batched_insert bulk_create.tests_llm.BatchedInsertBatchingTests.test_exact_division_batches bulk_create.tests_llm.BatchedInsertBatchingTests.test_inserted_rows_handling_list_and_single bulk_create.tests_llm.BatchedInsertBatchingTests.test_ops_return_zero_becomes_one
coverage json -o coverage.json
: '>>>>> End Test Output'
