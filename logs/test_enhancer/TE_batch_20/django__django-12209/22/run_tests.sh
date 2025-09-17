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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 serializers.models.test_data_llm.SaveDefaultPKTests.test_multiple_consecutive_force_update_saves serializers.models.test_data_llm.SaveDefaultPKTests.test_save_base_force_update_after_setting_other_attributes serializers.models.test_data_llm.SaveDefaultPKTests.test_save_base_force_update_in_transaction serializers.models.test_data_llm.SaveDefaultPKTests.test_save_base_force_update_simple serializers.models.test_data_llm.SaveDefaultPKTests.test_save_base_force_update_with_raw_true serializers.models.test_data_llm.SaveDefaultPKTests.test_save_base_force_update_with_using_default serializers.models.test_data_llm.SaveDefaultPKTests.test_save_force_update_after_setting_other_attributes serializers.models.test_data_llm.SaveDefaultPKTests.test_save_force_update_simple serializers.models.test_data_llm.SaveDefaultPKTests.test_save_force_update_with_raw_true serializers.models.test_data_llm.SaveDefaultPKTests.test_save_force_update_with_using_default
coverage json -o coverage.json
: '>>>>> End Test Output'
