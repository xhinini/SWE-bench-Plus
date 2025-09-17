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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 serializers.models.test_data_llm.FakeField.__init__ serializers.models.test_data_llm.FakeField.is_relation serializers.models.test_data_llm.FakeMeta.__init__ serializers.models.test_data_llm.SaveTableDecisionTests.test_force_insert_with_custom_pk_attname_calls_insert serializers.models.test_data_llm.SaveTableDecisionTests.test_force_insert_with_default_and_explicit_pk_provided_calls_insert serializers.models.test_data_llm.SaveTableDecisionTests.test_force_insert_with_default_callable_no_explicit_pk_calls_insert serializers.models.test_data_llm.SaveTableDecisionTests.test_force_insert_with_default_constant_no_explicit_pk_calls_insert serializers.models.test_data_llm.SaveTableDecisionTests.test_force_insert_with_multiple_non_pk_fields_calls_insert serializers.models.test_data_llm.SaveTableDecisionTests.test_force_insert_with_update_fields_using_attname_and_name_calls_insert serializers.models.test_data_llm.SaveTableDecisionTests.test_no_force_insert_when_default_is_not_provided serializers.models.test_data_llm.SaveTableDecisionTests.test_raw_true_does_not_force_insert_when_default_and_explicit_pk_uses_update serializers.models.test_data_llm.SaveTableDecisionTests.test_raw_true_does_not_force_insert_when_default_and_no_explicit_pk_uses_update serializers.models.test_data_llm.make_fake_instance
coverage json -o coverage.json
: '>>>>> End Test Output'
