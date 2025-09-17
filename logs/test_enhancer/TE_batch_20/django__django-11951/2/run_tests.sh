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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 bulk_create.tests_llm.BulkCreateBatchingTests.test_batch_size_equal_to_max bulk_create.tests_llm.BulkCreateBatchingTests.test_batch_size_larger_than_max_respected bulk_create.tests_llm.BulkCreateBatchingTests.test_batch_size_none_uses_max bulk_create.tests_llm.BulkCreateBatchingTests.test_batch_size_one_forces_one_query_per_object bulk_create.tests_llm.BulkCreateBatchingTests.test_empty_objs_performs_no_inserts bulk_create.tests_llm.BulkCreateBatchingTests.test_explicit_batch_size_respects_max_batch_size_again bulk_create.tests_llm.BulkCreateBatchingTests.test_ignore_conflicts_with_large_batch_size_respected bulk_create.tests_llm.BulkCreateBatchingTests.test_mixed_pk_and_no_pk_large_batch_size bulk_create.tests_llm.BulkCreateBatchingTests.test_returning_rows_multiple_batches_with_large_batch_size bulk_create.tests_llm.BulkCreateBatchingTests.test_very_large_batch_size_is_capped
coverage json -o coverage.json
: '>>>>> End Test Output'
