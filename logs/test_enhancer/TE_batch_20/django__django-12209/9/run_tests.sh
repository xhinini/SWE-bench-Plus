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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 serializers.models.test_data_llm.SaveTableRawBehaviorTests.setUp serializers.models.test_data_llm.SaveTableRawBehaviorTests.test_raw_false_with_default_pk_calls_insert_booleanpk serializers.models.test_data_llm.SaveTableRawBehaviorTests.test_raw_false_with_default_pk_calls_insert_uuid serializers.models.test_data_llm.SaveTableRawBehaviorTests.test_raw_false_with_explicit_pk_still_calls_insert_uuid serializers.models.test_data_llm.SaveTableRawBehaviorTests.test_raw_true_with_default_pk_calls_update_not_insert_booleanpk serializers.models.test_data_llm.SaveTableRawBehaviorTests.test_raw_true_with_default_pk_calls_update_not_insert_uuid serializers.models.test_data_llm.SaveTableRawBehaviorTests.test_raw_true_with_explicit_pk_calls_update_uuid serializers.models.test_data_llm.SaveTableRawBehaviorTests.test_save_base_raw_false_calls_insert_uuid serializers.models.test_data_llm.SaveTableRawBehaviorTests.test_save_base_raw_false_with_explicit_pk_calls_insert_uuid serializers.models.test_data_llm.SaveTableRawBehaviorTests.test_save_base_raw_true_calls_update_uuid serializers.models.test_data_llm.SaveTableRawBehaviorTests.test_save_base_raw_true_with_explicit_pk_calls_update_uuid serializers.models.test_data_llm._fake_do_insert serializers.models.test_data_llm._fake_do_update
coverage json -o coverage.json
: '>>>>> End Test Output'
