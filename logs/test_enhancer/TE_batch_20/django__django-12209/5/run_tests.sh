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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 serializers.models.test_data_llm.SaveRawPKDefaultTests.test_boolean_pk_default_multiple_raw_saves_do_not_create_duplicates serializers.models.test_data_llm.SaveRawPKDefaultTests.test_boolean_pk_default_save_base_raw_updates_existing serializers.models.test_data_llm.SaveRawPKDefaultTests.test_boolean_pk_default_save_raw_updates_existing serializers.models.test_data_llm.SaveRawPKDefaultTests.test_boolean_pk_default_save_raw_with_using_updates_existing serializers.models.test_data_llm.SaveRawPKDefaultTests.test_uuid_default_pk_multiple_raw_saves_do_not_create_duplicates serializers.models.test_data_llm.SaveRawPKDefaultTests.test_uuid_default_pk_save_base_raw_updates_existing serializers.models.test_data_llm.SaveRawPKDefaultTests.test_uuid_default_pk_save_base_raw_with_using_updates_existing serializers.models.test_data_llm.SaveRawPKDefaultTests.test_uuid_default_pk_save_raw_updates_existing serializers.models.test_data_llm.SaveRawPKDefaultTests.test_uuid_default_pk_save_raw_with_using_updates_existing
coverage json -o coverage.json
: '>>>>> End Test Output'
