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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 serializers.models.test_data_llm.ForceInsertOnDefaultPKTests._assert_save_forced_insert_raises serializers.models.test_data_llm.ForceInsertOnDefaultPKTests.test_boolean_pk_default_forced_insert_on_collision serializers.models.test_data_llm.ForceInsertOnDefaultPKTests.test_char_pk_default_forced_insert_on_collision serializers.models.test_data_llm.ForceInsertOnDefaultPKTests.test_date_pk_default_forced_insert_on_collision serializers.models.test_data_llm.ForceInsertOnDefaultPKTests.test_generic_ip_pk_default_forced_insert_on_collision serializers.models.test_data_llm.ForceInsertOnDefaultPKTests.test_integer_pk_default_forced_insert_on_collision serializers.models.test_data_llm.ForceInsertOnDefaultPKTests.test_positive_integer_pk_default_forced_insert_on_collision serializers.models.test_data_llm.ForceInsertOnDefaultPKTests.test_positive_small_integer_pk_default_forced_insert_on_collision serializers.models.test_data_llm.ForceInsertOnDefaultPKTests.test_slug_pk_default_forced_insert_on_collision serializers.models.test_data_llm.ForceInsertOnDefaultPKTests.test_smallinteger_pk_default_forced_insert_on_collision serializers.models.test_data_llm.ForceInsertOnDefaultPKTests.test_uuid_default_pk_forced_insert_on_collision
coverage json -o coverage.json
: '>>>>> End Test Output'
