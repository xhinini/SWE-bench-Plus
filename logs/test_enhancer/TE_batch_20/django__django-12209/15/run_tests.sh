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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 serializers.models.test_data_llm.RawSaveDefaultPKTests._assert_do_update_called serializers.models.test_data_llm.RawSaveDefaultPKTests.test_raw_save_calls_do_update_default_pk_01 serializers.models.test_data_llm.RawSaveDefaultPKTests.test_raw_save_calls_do_update_default_pk_02 serializers.models.test_data_llm.RawSaveDefaultPKTests.test_raw_save_calls_do_update_default_pk_03 serializers.models.test_data_llm.RawSaveDefaultPKTests.test_raw_save_calls_do_update_default_pk_04 serializers.models.test_data_llm.RawSaveDefaultPKTests.test_raw_save_calls_do_update_default_pk_05 serializers.models.test_data_llm.RawSaveDefaultPKTests.test_raw_save_calls_do_update_default_pk_06 serializers.models.test_data_llm.RawSaveDefaultPKTests.test_raw_save_calls_do_update_default_pk_07 serializers.models.test_data_llm.RawSaveDefaultPKTests.test_raw_save_calls_do_update_default_pk_08 serializers.models.test_data_llm.RawSaveDefaultPKTests.test_raw_save_calls_do_update_default_pk_09 serializers.models.test_data_llm.RawSaveDefaultPKTests.test_raw_save_calls_do_update_default_pk_10
coverage json -o coverage.json
: '>>>>> End Test Output'
