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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 bulk_create.tests_llm.BulkCreateBatchingRegressionTests.test_batch_size_capped_even_if_requested_much_larger_than_len bulk_create.tests_llm.BulkCreateBatchingRegressionTests.test_batch_size_equal_to_max bulk_create.tests_llm.BulkCreateBatchingRegressionTests.test_batch_size_exceeds_max_is_capped bulk_create.tests_llm.BulkCreateBatchingRegressionTests.test_batch_size_none_uses_max_batch_size bulk_create.tests_llm.BulkCreateBatchingRegressionTests.test_batch_size_smaller_than_max_is_used bulk_create.tests_llm.BulkCreateBatchingRegressionTests.test_bulk_batch_size_zero_becomes_one bulk_create.tests_llm.BulkCreateBatchingRegressionTests.test_can_return_rows_bulk_create_respects_capping bulk_create.tests_llm.BulkCreateBatchingRegressionTests.test_explicit_batch_size_one_respected bulk_create.tests_llm.BulkCreateBatchingRegressionTests.test_mixed_pk_and_no_pk_respects_max_batch_size bulk_create.tests_llm.BulkCreateBatchingRegressionTests.test_negative_bulk_batch_size_becomes_one
coverage json -o coverage.json
: '>>>>> End Test Output'
