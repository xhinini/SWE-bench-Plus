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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 serializers.models.test_data_llm.SaveTableRawPkDefaultTests._run_scenario serializers.models.test_data_llm.SaveTableRawPkDefaultTests.test_binarydata_raw_pk_default_uses_update_not_insert serializers.models.test_data_llm.SaveTableRawPkDefaultTests.test_booleanpkdata_raw_pk_default_uses_update_not_insert serializers.models.test_data_llm.SaveTableRawPkDefaultTests.test_chardata_raw_pk_default_uses_update_not_insert serializers.models.test_data_llm.SaveTableRawPkDefaultTests.test_datedata_raw_pk_default_uses_update_not_insert serializers.models.test_data_llm.SaveTableRawPkDefaultTests.test_emaildata_raw_pk_default_uses_update_not_insert serializers.models.test_data_llm.SaveTableRawPkDefaultTests.test_filepathdata_raw_pk_default_uses_update_not_insert serializers.models.test_data_llm.SaveTableRawPkDefaultTests.test_floatdata_raw_pk_default_uses_update_not_insert serializers.models.test_data_llm.SaveTableRawPkDefaultTests.test_integerdata_raw_pk_default_uses_update_not_insert serializers.models.test_data_llm.SaveTableRawPkDefaultTests.test_textdata_raw_pk_default_uses_update_not_insert serializers.models.test_data_llm.SaveTableRawPkDefaultTests.test_uuiddefaultdata_raw_pk_default_uses_update_not_insert
coverage json -o coverage.json
: '>>>>> End Test Output'
