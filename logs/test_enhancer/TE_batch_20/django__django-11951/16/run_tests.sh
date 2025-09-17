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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 bulk_create.tests_llm.BatchedInsertBatchingTests._make_objs bulk_create.tests_llm.BatchedInsertBatchingTests.test_batch_size_equal_to_backend_used bulk_create.tests_llm.BatchedInsertBatchingTests.test_batch_size_is_capped_to_backend_max bulk_create.tests_llm.BatchedInsertBatchingTests.test_batch_size_none_uses_backend_max bulk_create.tests_llm.BatchedInsertBatchingTests.test_batch_size_smaller_than_backend_used_as_is bulk_create.tests_llm.BatchedInsertBatchingTests.test_each_batch_never_exceeds_backend_max_even_if_backend_returns_zero bulk_create.tests_llm.BatchedInsertBatchingTests.test_mixed_objs_batches_respect_backend_max bulk_create.tests_llm.BatchedInsertBatchingTests.test_sum_of_batch_lengths_equals_total_for_various_backend_limits
coverage json -o coverage.json
: '>>>>> End Test Output'
