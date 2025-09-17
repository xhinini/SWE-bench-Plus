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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 serializers.models.test_data_llm.RawSaveForceInsertTests._run_raw_save_and_capture serializers.models.test_data_llm.RawSaveForceInsertTests.test_raw_save_calls_update_for_boolean_default_pk serializers.models.test_data_llm.RawSaveForceInsertTests.test_raw_save_calls_update_for_uuid_default_pk serializers.models.test_data_llm.RawSaveForceInsertTests.test_raw_save_calls_update_when_force_insert_false_boolean serializers.models.test_data_llm.RawSaveForceInsertTests.test_raw_save_calls_update_when_force_insert_false_uuid serializers.models.test_data_llm.RawSaveForceInsertTests.test_raw_save_calls_update_with_explicit_using_boolean serializers.models.test_data_llm.RawSaveForceInsertTests.test_raw_save_calls_update_with_explicit_using_uuid serializers.models.test_data_llm.RawSaveForceInsertTests.test_raw_save_calls_update_with_force_update_none_boolean serializers.models.test_data_llm.RawSaveForceInsertTests.test_raw_save_calls_update_with_force_update_none_uuid serializers.models.test_data_llm.RawSaveForceInsertTests.test_raw_save_calls_update_with_update_fields_none_boolean serializers.models.test_data_llm.RawSaveForceInsertTests.test_raw_save_calls_update_with_update_fields_none_uuid
coverage json -o coverage.json
: '>>>>> End Test Output'
