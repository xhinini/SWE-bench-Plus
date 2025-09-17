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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 serializers.models.test_data_llm.SaveTableRawDefaultPKTests._assert_update_called_for_raw_save serializers.models.test_data_llm.SaveTableRawDefaultPKTests.test_raw_save_attempts_update_after_setting_state_db serializers.models.test_data_llm.SaveTableRawDefaultPKTests.test_raw_save_attempts_update_default_pk serializers.models.test_data_llm.SaveTableRawDefaultPKTests.test_raw_save_attempts_update_if_pk_was_none_before_save serializers.models.test_data_llm.SaveTableRawDefaultPKTests.test_raw_save_attempts_update_regardless_of_attribute_mutation_before_call serializers.models.test_data_llm.SaveTableRawDefaultPKTests.test_raw_save_attempts_update_when_called_multiple_times serializers.models.test_data_llm.SaveTableRawDefaultPKTests.test_raw_save_attempts_update_when_state_adding_true serializers.models.test_data_llm.SaveTableRawDefaultPKTests.test_raw_save_attempts_update_when_update_returns_false serializers.models.test_data_llm.SaveTableRawDefaultPKTests.test_raw_save_attempts_update_when_update_returns_true serializers.models.test_data_llm.SaveTableRawDefaultPKTests.test_raw_save_attempts_update_with_explicit_using serializers.models.test_data_llm.SaveTableRawDefaultPKTests.test_raw_save_attempts_update_with_unusual_state_fields
coverage json -o coverage.json
: '>>>>> End Test Output'
