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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 serializers.models.test_data_llm.FakeField.__init__ serializers.models.test_data_llm.FakeField.pre_save serializers.models.test_data_llm.FakePK.__init__ serializers.models.test_data_llm.FakePK.get_pk_value_on_save serializers.models.test_data_llm.SaveTableBehaviorTests._run_save_table serializers.models.test_data_llm.SaveTableBehaviorTests.test_raw_false_with_empty_update_fields_bails_out serializers.models.test_data_llm.SaveTableBehaviorTests.test_raw_false_with_initial_pk_and_update_fields_skips_update serializers.models.test_data_llm.SaveTableBehaviorTests.test_raw_false_with_initial_pk_skips_update serializers.models.test_data_llm.SaveTableBehaviorTests.test_raw_false_with_no_initial_pk_skips_update serializers.models.test_data_llm.SaveTableBehaviorTests.test_raw_false_with_update_fields_skips_update serializers.models.test_data_llm.SaveTableBehaviorTests.test_raw_true_with_empty_update_fields_calls_update serializers.models.test_data_llm.SaveTableBehaviorTests.test_raw_true_with_initial_pk_and_update_fields_calls_update serializers.models.test_data_llm.SaveTableBehaviorTests.test_raw_true_with_initial_pk_calls_update serializers.models.test_data_llm.SaveTableBehaviorTests.test_raw_true_with_no_initial_pk_calls_update serializers.models.test_data_llm.SaveTableBehaviorTests.test_raw_true_with_update_fields_calls_update
coverage json -o coverage.json
: '>>>>> End Test Output'
