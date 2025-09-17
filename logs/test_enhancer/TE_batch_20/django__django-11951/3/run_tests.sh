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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 bulk_create.tests_llm.BulkCreateBatchSizeRegressionTests.test_batched_insert_respects_max_batch_size_non_returning_mixed_pk bulk_create.tests_llm.BulkCreateBatchSizeRegressionTests.test_batched_insert_respects_max_batch_size_non_returning_no_pk bulk_create.tests_llm.BulkCreateBatchSizeRegressionTests.test_batched_insert_respects_max_batch_size_returning_mixed_pk bulk_create.tests_llm.BulkCreateBatchSizeRegressionTests.test_batched_insert_respects_max_batch_size_returning_no_pk bulk_create.tests_llm.BulkCreateBatchSizeRegressionTests.test_batched_insert_treats_zero_max_batch_size_as_one bulk_create.tests_llm.BulkCreateBatchSizeRegressionTests.test_batched_insert_uses_provided_batch_size_when_less_than_max bulk_create.tests_llm.BulkCreateBatchSizeRegressionTests.test_combined_returning_and_ignore_conflicts_respects_max_batch_size bulk_create.tests_llm.BulkCreateBatchSizeRegressionTests.test_explicit_batch_size_equal_to_max_is_honored bulk_create.tests_llm.BulkCreateBatchSizeRegressionTests.test_ignore_conflicts_raises_when_not_supported bulk_create.tests_llm.BulkCreateBatchSizeRegressionTests.test_ignore_conflicts_respects_max_batch_size_when_supported
coverage json -o coverage.json
: '>>>>> End Test Output'
