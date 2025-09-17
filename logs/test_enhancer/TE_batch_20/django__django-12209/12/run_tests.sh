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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 serializers.models.test_data_llm.SavePKDefaultRegressionTests.test_boolpk_save_base_force_update_with_explicit_pk serializers.models.test_data_llm.SavePKDefaultRegressionTests.test_boolpk_save_base_update_fields_with_explicit_pk serializers.models.test_data_llm.SavePKDefaultRegressionTests.test_boolpk_save_force_update_and_update_fields_with_explicit_pk serializers.models.test_data_llm.SavePKDefaultRegressionTests.test_boolpk_save_force_update_with_explicit_pk serializers.models.test_data_llm.SavePKDefaultRegressionTests.test_boolpk_save_update_fields_with_explicit_pk serializers.models.test_data_llm.SavePKDefaultRegressionTests.test_uuid_save_base_force_update_with_explicit_pk serializers.models.test_data_llm.SavePKDefaultRegressionTests.test_uuid_save_base_update_fields_with_explicit_pk serializers.models.test_data_llm.SavePKDefaultRegressionTests.test_uuid_save_force_update_and_update_fields_with_explicit_pk serializers.models.test_data_llm.SavePKDefaultRegressionTests.test_uuid_save_force_update_with_explicit_pk serializers.models.test_data_llm.SavePKDefaultRegressionTests.test_uuid_save_update_fields_with_explicit_pk
coverage json -o coverage.json
: '>>>>> End Test Output'
