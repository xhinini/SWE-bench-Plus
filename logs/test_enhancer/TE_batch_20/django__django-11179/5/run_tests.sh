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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 delete.tests_llm.FastDeletePkNullingTests._create_model delete.tests_llm.FastDeletePkNullingTests.test_auto_pk_model_delete_sets_pk_none_and_returns_counts delete.tests_llm.FastDeletePkNullingTests.test_charfield_pk_model_delete_sets_pk_none_and_returns_counts delete.tests_llm.FastDeletePkNullingTests.test_custom_attname_pk_model_delete_sets_attname_none delete.tests_llm.FastDeletePkNullingTests.test_db_column_pk_model_delete_sets_attname_none delete.tests_llm.FastDeletePkNullingTests.test_delete_on_many_instances_only_affects_instance_deleted delete.tests_llm.FastDeletePkNullingTests.test_delete_returns_expected_mapping_key delete.tests_llm.FastDeletePkNullingTests.test_delete_sets_pk_none_for_big_auto_field delete.tests_llm.FastDeletePkNullingTests.test_delete_sets_pk_none_for_uuid_char_pk delete.tests_llm.FastDeletePkNullingTests.test_delete_sets_pk_none_when_no_extra_fields delete.tests_llm.FastDeletePkNullingTests.test_delete_twice_leaves_pk_none_and_no_error
coverage json -o coverage.json
: '>>>>> End Test Output'
