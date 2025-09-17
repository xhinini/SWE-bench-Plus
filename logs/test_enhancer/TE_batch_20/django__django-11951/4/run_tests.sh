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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 bulk_create.tests_llm.BulkCreateBatchingTests.test_batched_empty_objs_no_queries bulk_create.tests_llm.BulkCreateBatchingTests.test_batched_handles_zero_max_batch_size bulk_create.tests_llm.BulkCreateBatchingTests.test_batched_large_single_field_batch_respects_max bulk_create.tests_llm.BulkCreateBatchingTests.test_batched_mixed_pk_respects_max bulk_create.tests_llm.BulkCreateBatchingTests.test_batched_provided_equals_max bulk_create.tests_llm.BulkCreateBatchingTests.test_batched_provided_less_than_max bulk_create.tests_llm.BulkCreateBatchingTests.test_batched_respects_max_explicit_too_large bulk_create.tests_llm.BulkCreateBatchingTests.test_batched_uses_max_when_batch_none bulk_create.tests_llm.BulkCreateBatchingTests.test_batched_uses_smaller_provided_batch bulk_create.tests_llm.BulkCreateBatchingTests.test_explicit_batch_size_respects_max_batch_size_with_one
coverage json -o coverage.json
: '>>>>> End Test Output'
