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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 serializers.models.test_data_llm.SaveTableRawPkDefaultTests._run_save_table_and_capture serializers.models.test_data_llm.SaveTableRawPkDefaultTests.test_booleanpk_default_raw_consistency serializers.models.test_data_llm.SaveTableRawPkDefaultTests.test_booleanpk_default_raw_using_default_updatefields_none serializers.models.test_data_llm.SaveTableRawPkDefaultTests.test_booleanpk_default_raw_using_none_updatefields_none serializers.models.test_data_llm.SaveTableRawPkDefaultTests.test_booleanpk_default_raw_with_default_using_and_updatefields serializers.models.test_data_llm.SaveTableRawPkDefaultTests.test_booleanpk_default_raw_with_update_fields serializers.models.test_data_llm.SaveTableRawPkDefaultTests.test_uuid_default_raw_using_default_updatefields_none serializers.models.test_data_llm.SaveTableRawPkDefaultTests.test_uuid_default_raw_using_default_with_update_fields serializers.models.test_data_llm.SaveTableRawPkDefaultTests.test_uuid_default_raw_using_none_forceupdate_false serializers.models.test_data_llm.SaveTableRawPkDefaultTests.test_uuid_default_raw_using_none_updatefields_none serializers.models.test_data_llm.SaveTableRawPkDefaultTests.test_uuid_default_raw_using_none_with_update_fields
coverage json -o coverage.json
: '>>>>> End Test Output'
