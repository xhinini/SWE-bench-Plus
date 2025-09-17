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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 delete.tests_llm.AdditionalFastDeletePKTests._create_model_and_table delete.tests_llm.AdditionalFastDeletePKTests._delete_table delete.tests_llm.AdditionalFastDeletePKTests.test_auto_field_pk_cleared_after_model_delete delete.tests_llm.AdditionalFastDeletePKTests.test_auto_field_pk_cleared_after_model_delete_when_refetched delete.tests_llm.AdditionalFastDeletePKTests.test_char_pk_cleared_after_model_delete_when_refetched delete.tests_llm.AdditionalFastDeletePKTests.test_charfield_pk_cleared_after_model_delete delete.tests_llm.AdditionalFastDeletePKTests.test_explicit_integer_pk_cleared_after_model_delete delete.tests_llm.AdditionalFastDeletePKTests.test_multiple_auto_models_each_pk_cleared_after_individual_delete delete.tests_llm.AdditionalFastDeletePKTests.test_pk_cleared_after_delete_for_explicitly_assigned_autofield_like_value delete.tests_llm.AdditionalFastDeletePKTests.test_pk_cleared_after_delete_for_model_with_long_char_pk_value delete.tests_llm.AdditionalFastDeletePKTests.test_pk_cleared_after_delete_when_primary_key_is_boolean_like_integer delete.tests_llm.AdditionalFastDeletePKTests.test_uuidfield_pk_cleared_after_model_delete
coverage json -o coverage.json
: '>>>>> End Test Output'
