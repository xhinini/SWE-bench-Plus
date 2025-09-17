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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 bulk_create.tests_llm.BulkCreateBatchingRegressionTests.test_batched_insert_aggregates_returned_rows_across_batches bulk_create.tests_llm.BulkCreateBatchingRegressionTests.test_batched_insert_limits_batch_size_when_explicit_size_exceeds_max bulk_create.tests_llm.BulkCreateBatchingRegressionTests.test_batched_insert_mixed_pk_objects_with_large_batch_size bulk_create.tests_llm.BulkCreateBatchingRegressionTests.test_batched_insert_respects_smaller_batch_size bulk_create.tests_llm.BulkCreateBatchingRegressionTests.test_batched_insert_uses_max_when_batch_size_none bulk_create.tests_llm.BulkCreateBatchingRegressionTests.test_explicit_batch_size_equal_to_max_batch_size_results_in_expected_number_of_queries bulk_create.tests_llm.BulkCreateBatchingRegressionTests.test_ignore_conflicts_large_batch_respects_max_batch_size bulk_create.tests_llm.BulkCreateBatchingRegressionTests.test_multiple_calls_with_varying_batch_sizes_obey_limits_each_time bulk_create.tests_llm.BulkCreateBatchingRegressionTests.test_ops_bulk_batch_size_one_forces_single_item_per_batch_even_if_large_batch_requested bulk_create.tests_llm.BulkCreateBatchingRegressionTests.test_ops_bulk_batch_size_zero_is_treated_as_one
coverage json -o coverage.json
: '>>>>> End Test Output'
