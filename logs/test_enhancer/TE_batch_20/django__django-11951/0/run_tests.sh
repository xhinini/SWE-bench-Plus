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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 bulk_create.tests_llm.BulkCreateBatchingTests.test_batched_insert_caps_explicit_batch_size_larger_than_max bulk_create.tests_llm.BulkCreateBatchingTests.test_batched_insert_caps_when_ops_returns_zero_and_explicit_large bulk_create.tests_llm.BulkCreateBatchingTests.test_batched_insert_exact_division bulk_create.tests_llm.BulkCreateBatchingTests.test_batched_insert_many_small_batches bulk_create.tests_llm.BulkCreateBatchingTests.test_batched_insert_minimum_one_when_ops_returns_zero_and_none bulk_create.tests_llm.BulkCreateBatchingTests.test_batched_insert_mixed_pk_counts_queries bulk_create.tests_llm.BulkCreateBatchingTests.test_batched_insert_respects_max_batch_size_with_different_model bulk_create.tests_llm.BulkCreateBatchingTests.test_batched_insert_single_batch_when_batch_size_large_enough bulk_create.tests_llm.BulkCreateBatchingTests.test_batched_insert_uses_max_when_batch_size_none bulk_create.tests_llm.BulkCreateBatchingTests.test_batched_insert_uses_provided_batch_size_if_smaller_than_max
coverage json -o coverage.json
: '>>>>> End Test Output'
