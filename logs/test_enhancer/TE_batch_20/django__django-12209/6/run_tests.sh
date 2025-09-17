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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 serializers.models.test_data_llm.FakeManager.using serializers.models.test_data_llm.FakePK.__init__ serializers.models.test_data_llm.FakePK.get_pk_value_on_save serializers.models.test_data_llm.SaveTableRawFlagTests.assert_insert_called serializers.models.test_data_llm.SaveTableRawFlagTests.assert_update_called serializers.models.test_data_llm.SaveTableRawFlagTests.test_raw_false_int_default_calls_insert serializers.models.test_data_llm.SaveTableRawFlagTests.test_raw_false_uuid_default_calls_insert serializers.models.test_data_llm.SaveTableRawFlagTests.test_raw_false_with_explicit_pk_calls_insert serializers.models.test_data_llm.SaveTableRawFlagTests.test_raw_true_bool_callable_default_calls_update serializers.models.test_data_llm.SaveTableRawFlagTests.test_raw_true_callable_returning_object_calls_update serializers.models.test_data_llm.SaveTableRawFlagTests.test_raw_true_int_default_calls_update serializers.models.test_data_llm.SaveTableRawFlagTests.test_raw_true_lambda_default_calls_update serializers.models.test_data_llm.SaveTableRawFlagTests.test_raw_true_str_callable_default_calls_update serializers.models.test_data_llm.SaveTableRawFlagTests.test_raw_true_uuid_default_callable_calls_update serializers.models.test_data_llm.SaveTableRawFlagTests.test_raw_true_with_explicit_pk_calls_update serializers.models.test_data_llm.make_fake_class_and_instance
coverage json -o coverage.json
: '>>>>> End Test Output'
