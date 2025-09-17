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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 serializers.models.test_data_llm.SaveTableRawTests._patch_instance_do_methods serializers.models.test_data_llm.SaveTableRawTests.test_non_raw_falsepath_calls_do_update_and_insert_as_expected serializers.models.test_data_llm.SaveTableRawTests.test_raw_true_attempts_update_even_if_pk_was_filled_by_default serializers.models.test_data_llm.SaveTableRawTests.test_raw_true_both_update_and_insert_called_when_update_returns_false serializers.models.test_data_llm.SaveTableRawTests.test_raw_true_calls_do_update_for_boolean_pk_with_default serializers.models.test_data_llm.SaveTableRawTests.test_raw_true_calls_do_update_for_uuid_default_pk serializers.models.test_data_llm.SaveTableRawTests.test_raw_true_calls_do_update_for_uuid_related_model_instance serializers.models.test_data_llm.SaveTableRawTests.test_raw_true_calls_do_update_when_metadata_local_concrete_fields_present serializers.models.test_data_llm.SaveTableRawTests.test_raw_true_calls_do_update_when_update_fields_and_pk_attname_included serializers.models.test_data_llm.SaveTableRawTests.test_raw_true_with_existing_attribute_values_triggers_do_update serializers.models.test_data_llm.SaveTableRawTests.test_raw_true_with_update_fields_calls_do_update
coverage json -o coverage.json
: '>>>>> End Test Output'
