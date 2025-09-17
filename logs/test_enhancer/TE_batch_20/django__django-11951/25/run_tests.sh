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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 bulk_create.tests_llm.BulkCreateBatchSizeRegressionTests.test_batch_size_larger_than_max_uses_max bulk_create.tests_llm.BulkCreateBatchSizeRegressionTests.test_batch_size_smaller_than_max_uses_given bulk_create.tests_llm.BulkCreateBatchSizeRegressionTests.test_batch_size_zero_raises_assertion bulk_create.tests_llm.BulkCreateBatchSizeRegressionTests.test_bulk_batch_size_zero_treated_as_one bulk_create.tests_llm.BulkCreateBatchSizeRegressionTests.test_ignore_conflicts_respects_max_batch_size bulk_create.tests_llm.BulkCreateBatchSizeRegressionTests.test_mixed_with_and_without_pk_respects_computed_for_each_group bulk_create.tests_llm.BulkCreateBatchSizeRegressionTests.test_none_batch_size_uses_max bulk_create.tests_llm.BulkCreateBatchSizeRegressionTests.test_none_batch_size_with_ops_returning_zero_acts_as_one bulk_create.tests_llm.BulkCreateBatchSizeRegressionTests.test_restaurant_single_field_large_batch_respects_max
coverage json -o coverage.json
: '>>>>> End Test Output'
