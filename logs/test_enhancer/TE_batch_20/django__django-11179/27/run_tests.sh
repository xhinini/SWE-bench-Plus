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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 delete.tests_llm.FastDeletePKClearTests._create_model delete.tests_llm.FastDeletePKClearTests.test_auto_field_pk_cleared_after_model_delete delete.tests_llm.FastDeletePKClearTests.test_charfield_primary_key_cleared_after_model_delete delete.tests_llm.FastDeletePKClearTests.test_custom_attname_primary_key_cleared_after_model_delete delete.tests_llm.FastDeletePKClearTests.test_delete_returns_expected_counts_and_clears_pk_for_custom_pk_name delete.tests_llm.FastDeletePKClearTests.test_deleting_single_object_with_non_id_attname_clears_underlying_attname delete.tests_llm.FastDeletePKClearTests.test_multiple_sequential_creates_and_deletes_clear_pk_each_time delete.tests_llm.FastDeletePKClearTests.test_onetoone_primary_key_cleared_after_model_delete delete.tests_llm.FastDeletePKClearTests.test_other_fields_unchanged_when_pk_cleared_after_delete delete.tests_llm.FastDeletePKClearTests.test_uuidfield_primary_key_cleared_after_model_delete
coverage json -o coverage.json
: '>>>>> End Test Output'
