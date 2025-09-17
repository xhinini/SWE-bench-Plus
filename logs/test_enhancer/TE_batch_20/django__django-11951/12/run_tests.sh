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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 bulk_create.tests_llm.BulkCreateTests.test_batch_size_clamped_to_ops_bulk_batch_size_patch_countries bulk_create.tests_llm.BulkCreateTests.test_batch_size_clamped_to_ops_bulk_batch_size_patch_twofields bulk_create.tests_llm.BulkCreateTests.test_batch_size_negative_raises_assertion bulk_create.tests_llm.BulkCreateTests.test_batch_size_zero_raises_assertion bulk_create.tests_llm.BulkCreateTests.test_batched_insert_splits_into_multiple_batches bulk_create.tests_llm.BulkCreateTests.test_explicit_small_batch_size_used_when_less_than_max bulk_create.tests_llm.BulkCreateTests.test_ignore_conflicts_with_large_batch_clamped_patch bulk_create.tests_llm.BulkCreateTests.test_mixed_pk_large_batch_clamped_patch bulk_create.tests_llm.BulkCreateTests.test_none_batch_size_uses_ops_bulk_batch_size_patch
coverage json -o coverage.json
: '>>>>> End Test Output'
