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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 bulk_create.tests_llm.BulkCreateTests.setUp bulk_create.tests_llm.BulkCreateTests.test_batched_insert_batch_size_equal_to_max_uses_that_size bulk_create.tests_llm.BulkCreateTests.test_batched_insert_caps_explicit_batch_size_when_larger_bulk_return_false bulk_create.tests_llm.BulkCreateTests.test_batched_insert_caps_explicit_batch_size_when_larger_bulk_return_true bulk_create.tests_llm.BulkCreateTests.test_batched_insert_collects_returned_rows_in_single_batch bulk_create.tests_llm.BulkCreateTests.test_batched_insert_ensures_minimum_max_batch_size_of_one bulk_create.tests_llm.BulkCreateTests.test_batched_insert_raises_not_supported_error_when_ignore_conflicts_unsupported bulk_create.tests_llm.BulkCreateTests.test_batched_insert_single_small_batch_when_explicit_large_but_capped bulk_create.tests_llm.BulkCreateTests.test_batched_insert_uses_explicit_batch_size_when_smaller_than_max bulk_create.tests_llm.BulkCreateTests.test_batched_insert_uses_max_when_batch_size_is_none
coverage json -o coverage.json
: '>>>>> End Test Output'
