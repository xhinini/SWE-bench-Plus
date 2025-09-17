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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 serializers.models.test_data_llm.RawSaveDefaultPKTests.setUp serializers.models.test_data_llm.RawSaveDefaultPKTests.tearDown serializers.models.test_data_llm.RawSaveDefaultPKTests.test_raw_save_does_not_call_insert_01 serializers.models.test_data_llm.RawSaveDefaultPKTests.test_raw_save_does_not_call_insert_02 serializers.models.test_data_llm.RawSaveDefaultPKTests.test_raw_save_does_not_call_insert_03 serializers.models.test_data_llm.RawSaveDefaultPKTests.test_raw_save_does_not_call_insert_04 serializers.models.test_data_llm.RawSaveDefaultPKTests.test_raw_save_does_not_call_insert_05 serializers.models.test_data_llm.RawSaveDefaultPKTests.test_raw_save_does_not_call_insert_06 serializers.models.test_data_llm.RawSaveDefaultPKTests.test_raw_save_does_not_call_insert_07 serializers.models.test_data_llm.RawSaveDefaultPKTests.test_raw_save_does_not_call_insert_08 serializers.models.test_data_llm.RawSaveDefaultPKTests.test_raw_save_does_not_call_insert_09 serializers.models.test_data_llm.RawSaveDefaultPKTests.test_raw_save_does_not_call_insert_10
coverage json -o coverage.json
: '>>>>> End Test Output'
