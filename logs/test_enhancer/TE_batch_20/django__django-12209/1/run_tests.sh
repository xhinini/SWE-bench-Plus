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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 serializers.models.test_data_llm.SaveRawPkDefaultRegressionTests._run_save_base_and_capture serializers.models.test_data_llm.SaveRawPkDefaultRegressionTests.test_raw_true_boolean_pk_default_triggers_update serializers.models.test_data_llm.SaveRawPkDefaultRegressionTests.test_raw_true_boolean_pk_default_with_force_update_triggers_update_attempt serializers.models.test_data_llm.SaveRawPkDefaultRegressionTests.test_raw_true_boolean_pk_default_with_nonpk_set_triggers_update_attempt serializers.models.test_data_llm.SaveRawPkDefaultRegressionTests.test_raw_true_boolean_pk_default_with_update_fields_triggers_update_attempt serializers.models.test_data_llm.SaveRawPkDefaultRegressionTests.test_raw_true_boolean_pk_default_with_using_triggers_update serializers.models.test_data_llm.SaveRawPkDefaultRegressionTests.test_raw_true_uuid_default_triggers_update serializers.models.test_data_llm.SaveRawPkDefaultRegressionTests.test_raw_true_uuid_default_with_force_update_triggers_update_attempt serializers.models.test_data_llm.SaveRawPkDefaultRegressionTests.test_raw_true_uuid_default_with_nonpk_set_triggers_update_attempt serializers.models.test_data_llm.SaveRawPkDefaultRegressionTests.test_raw_true_uuid_default_with_update_fields_triggers_update_attempt serializers.models.test_data_llm.SaveRawPkDefaultRegressionTests.test_raw_true_uuid_default_with_using_triggers_update
coverage json -o coverage.json
: '>>>>> End Test Output'
