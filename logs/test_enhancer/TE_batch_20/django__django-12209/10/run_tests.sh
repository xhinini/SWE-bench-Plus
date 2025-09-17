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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 serializers.models.test_data_llm.SaveWithDefaultPKTests._new_instance_with_explicit_pk serializers.models.test_data_llm.SaveWithDefaultPKTests.setUp serializers.models.test_data_llm.SaveWithDefaultPKTests.test_save_with_force_update_true_inserts_new_instance serializers.models.test_data_llm.SaveWithDefaultPKTests.test_save_with_update_fields_and_force_update_and_using_inserts serializers.models.test_data_llm.SaveWithDefaultPKTests.test_save_with_update_fields_and_force_update_true_inserts serializers.models.test_data_llm.SaveWithDefaultPKTests.test_save_with_update_fields_and_raw_false_inserts serializers.models.test_data_llm.SaveWithDefaultPKTests.test_save_with_update_fields_and_using_and_raw_inserts serializers.models.test_data_llm.SaveWithDefaultPKTests.test_save_with_update_fields_frozenset_inserts_new_instance serializers.models.test_data_llm.SaveWithDefaultPKTests.test_save_with_update_fields_list_inserts_new_instance serializers.models.test_data_llm.SaveWithDefaultPKTests.test_save_with_update_fields_set_inserts_new_instance serializers.models.test_data_llm.SaveWithDefaultPKTests.test_save_with_update_fields_tuple_inserts_new_instance serializers.models.test_data_llm.SaveWithDefaultPKTests.test_save_with_update_fields_using_default_db_inserts
coverage json -o coverage.json
: '>>>>> End Test Output'
