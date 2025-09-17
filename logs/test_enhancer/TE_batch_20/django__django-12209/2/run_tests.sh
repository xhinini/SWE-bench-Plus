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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 serializers.models.test_data_llm.RawSaveDefaultPKTests._assert_raw_save_updates_existing serializers.models.test_data_llm.RawSaveDefaultPKTests.test_booleanpk_default_raw_save_called_twice serializers.models.test_data_llm.RawSaveDefaultPKTests.test_booleanpk_default_raw_save_no_integrity_error serializers.models.test_data_llm.RawSaveDefaultPKTests.test_booleanpk_default_raw_save_updates_existing serializers.models.test_data_llm.RawSaveDefaultPKTests.test_booleanpk_default_raw_save_updates_existing_in_atomic serializers.models.test_data_llm.RawSaveDefaultPKTests.test_uuid_default_raw_save_no_integrity_error serializers.models.test_data_llm.RawSaveDefaultPKTests.test_uuid_default_raw_save_updates_existing serializers.models.test_data_llm.RawSaveDefaultPKTests.test_uuid_default_raw_save_updates_existing_in_atomic serializers.models.test_data_llm.RawSaveDefaultPKTests.test_uuid_default_raw_save_updates_existing_when_called_twice serializers.models.test_data_llm.RawSaveDefaultPKTests.test_uuid_default_raw_save_with_using_default
coverage json -o coverage.json
: '>>>>> End Test Output'
