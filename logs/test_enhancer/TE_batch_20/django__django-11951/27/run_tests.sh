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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 bulk_create.tests_llm.BatchedInsertBatchingTests._run_batched_insert_with_fake_insert bulk_create.tests_llm.BatchedInsertBatchingTests.test_backend_bulk_batch_size_zero_treated_as_at_least_one bulk_create.tests_llm.BatchedInsertBatchingTests.test_batch_size_equal_to_max_behaves_normally bulk_create.tests_llm.BatchedInsertBatchingTests.test_batch_size_larger_than_needed_but_clamped bulk_create.tests_llm.BatchedInsertBatchingTests.test_bulk_return_false_collects_no_returned_rows bulk_create.tests_llm.BatchedInsertBatchingTests.test_empty_objs_results_in_no_calls bulk_create.tests_llm.BatchedInsertBatchingTests.test_non_auto_pk_model_respects_max_batch_size bulk_create.tests_llm.BatchedInsertBatchingTests.test_none_batch_size_uses_backend_max bulk_create.tests_llm.BatchedInsertBatchingTests.test_not_supported_ignore_conflicts_raises bulk_create.tests_llm.BatchedInsertBatchingTests.test_requested_larger_than_max_is_clamped_to_max bulk_create.tests_llm.BatchedInsertBatchingTests.test_requested_smaller_than_max_uses_requested
coverage json -o coverage.json
: '>>>>> End Test Output'
