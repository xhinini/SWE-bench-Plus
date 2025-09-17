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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 bulk_create.tests_llm.BulkCreateBatchingRegressionTests._patch_bulk_batch_size bulk_create.tests_llm.BulkCreateBatchingRegressionTests.test_batch_size_smaller_than_max_not_changed bulk_create.tests_llm.BulkCreateBatchingRegressionTests.test_batching_on_different_model_respects_max bulk_create.tests_llm.BulkCreateBatchingRegressionTests.test_batching_with_returning_rows_feature bulk_create.tests_llm.BulkCreateBatchingRegressionTests.test_explicit_batch_size_greater_than_max_is_capped bulk_create.tests_llm.BulkCreateBatchingRegressionTests.test_large_batch_exact_multiple_of_max bulk_create.tests_llm.BulkCreateBatchingRegressionTests.test_large_batch_not_exact_multiple_of_max bulk_create.tests_llm.BulkCreateBatchingRegressionTests.test_mixed_with_and_without_pk_respects_max_batch_size bulk_create.tests_llm.BulkCreateBatchingRegressionTests.test_no_batch_size_uses_max_batch_size bulk_create.tests_llm.BulkCreateBatchingRegressionTests.test_ops_bulk_batch_size_negative_treated_as_one bulk_create.tests_llm.BulkCreateBatchingRegressionTests.test_ops_bulk_batch_size_zero_treated_as_one
coverage json -o coverage.json
: '>>>>> End Test Output'
