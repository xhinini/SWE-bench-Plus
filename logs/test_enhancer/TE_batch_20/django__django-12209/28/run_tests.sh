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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 serializers.models.test_data_llm.SaveTableForceInsertTests._run_save_table_expect_insert serializers.models.test_data_llm.SaveTableForceInsertTests.test_boolean_pk_default_forces_insert_with_force_update_and_update_fields serializers.models.test_data_llm.SaveTableForceInsertTests.test_boolean_pk_default_forces_insert_with_force_update_true serializers.models.test_data_llm.SaveTableForceInsertTests.test_boolean_pk_default_forces_insert_with_update_fields serializers.models.test_data_llm.SaveTableForceInsertTests.test_explicit_boolean_pk_still_inserts_when_adding_and_forced_update serializers.models.test_data_llm.SaveTableForceInsertTests.test_explicit_uuid_pk_still_inserts_when_adding_and_forced_update serializers.models.test_data_llm.SaveTableForceInsertTests.test_uuid_default_pk_forces_insert_when_force_insert_param_true serializers.models.test_data_llm.SaveTableForceInsertTests.test_uuid_default_pk_forces_insert_with_force_update_true serializers.models.test_data_llm.SaveTableForceInsertTests.test_uuid_default_pk_forces_insert_with_update_fields serializers.models.test_data_llm.SaveTableForceInsertTests.test_uuid_default_pk_forces_insert_with_update_fields_and_force_insert_false serializers.models.test_data_llm.SaveTableForceInsertTests.test_uuid_default_pk_forces_insert_with_update_fields_attname
coverage json -o coverage.json
: '>>>>> End Test Output'
