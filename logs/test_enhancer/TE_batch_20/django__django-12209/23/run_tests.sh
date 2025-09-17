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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 serializers.models.test_data_llm.SaveRawPkDefaultTests._spy_save serializers.models.test_data_llm.SaveRawPkDefaultTests.test_boolean_pk_default_raw_save_direct_save_method_with_explicit_pk serializers.models.test_data_llm.SaveRawPkDefaultTests.test_boolean_pk_default_raw_save_uses_update_attempt serializers.models.test_data_llm.SaveRawPkDefaultTests.test_boolean_pk_default_raw_save_via_save_uses_update_attempt serializers.models.test_data_llm.SaveRawPkDefaultTests.test_boolean_pk_default_raw_save_with_explicit_pk_attempts_update serializers.models.test_data_llm.SaveRawPkDefaultTests.test_boolean_pk_default_raw_save_without_using_uses_update_attempt serializers.models.test_data_llm.SaveRawPkDefaultTests.test_uuid_default_raw_save_direct_save_method_with_explicit_pk serializers.models.test_data_llm.SaveRawPkDefaultTests.test_uuid_default_raw_save_uses_update_attempt serializers.models.test_data_llm.SaveRawPkDefaultTests.test_uuid_default_raw_save_via_save_uses_update_attempt serializers.models.test_data_llm.SaveRawPkDefaultTests.test_uuid_default_raw_save_with_explicit_pk_attempts_update serializers.models.test_data_llm.SaveRawPkDefaultTests.test_uuid_default_raw_save_without_using_uses_update_attempt
coverage json -o coverage.json
: '>>>>> End Test Output'
