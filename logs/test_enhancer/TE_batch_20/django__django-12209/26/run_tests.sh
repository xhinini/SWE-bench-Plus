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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 serializers.models.test_data_llm.SaveRawPKDefaultTests._make_instance_and_patch serializers.models.test_data_llm.SaveRawPKDefaultTests.test_int_default_raw_calls_do_update_with_force_update_true serializers.models.test_data_llm.SaveRawPKDefaultTests.test_int_default_raw_calls_do_update_with_update_fields serializers.models.test_data_llm.SaveRawPKDefaultTests.test_uuid_default_raw_calls_do_update_with_force_update_true serializers.models.test_data_llm.SaveRawPKDefaultTests.test_uuid_default_raw_calls_do_update_with_update_fields serializers.models.test_data_llm.SaveRawPKDefaultTests.test_uuid_default_raw_calls_do_update_with_update_fields_attname
coverage json -o coverage.json
: '>>>>> End Test Output'
