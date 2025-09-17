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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 serializers.models.test_data_llm.SaveWithPKDefaultTests._destroy_temp_model serializers.models.test_data_llm.SaveWithPKDefaultTests._make_temp_model serializers.models.test_data_llm.SaveWithPKDefaultTests._save_with_update_fields_and_assert serializers.models.test_data_llm.SaveWithPKDefaultTests.test_save_with_update_fields_as_tuple_of_one serializers.models.test_data_llm.SaveWithPKDefaultTests.test_save_with_update_fields_explicit_pk_provided serializers.models.test_data_llm.SaveWithPKDefaultTests.test_save_with_update_fields_frozenset serializers.models.test_data_llm.SaveWithPKDefaultTests.test_save_with_update_fields_frozenset_explicit_pk serializers.models.test_data_llm.SaveWithPKDefaultTests.test_save_with_update_fields_generator serializers.models.test_data_llm.SaveWithPKDefaultTests.test_save_with_update_fields_iter serializers.models.test_data_llm.SaveWithPKDefaultTests.test_save_with_update_fields_list serializers.models.test_data_llm.SaveWithPKDefaultTests.test_save_with_update_fields_set serializers.models.test_data_llm.SaveWithPKDefaultTests.test_save_with_update_fields_single_string_in_list serializers.models.test_data_llm.SaveWithPKDefaultTests.test_save_with_update_fields_tuple
coverage json -o coverage.json
: '>>>>> End Test Output'
