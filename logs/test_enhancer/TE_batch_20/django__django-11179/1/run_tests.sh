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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 delete.tests_llm.FastDeleteEarlyReturnRegressionTests._destroy_dynamic_model delete.tests_llm.FastDeleteEarlyReturnRegressionTests._make_dynamic_model delete.tests_llm.FastDeleteEarlyReturnRegressionTests.test_auto_pk_model_delete_multiple_calls_consistent delete.tests_llm.FastDeleteEarlyReturnRegressionTests.test_auto_pk_model_delete_sets_pk_none delete.tests_llm.FastDeleteEarlyReturnRegressionTests.test_custom_char_pk_model_delete_sets_pk_none delete.tests_llm.FastDeleteEarlyReturnRegressionTests.test_custom_int_pk_field_with_name_not_id_sets_pk_none delete.tests_llm.FastDeleteEarlyReturnRegressionTests.test_delete_does_not_set_pk_if_delete_fails delete.tests_llm.FastDeleteEarlyReturnRegressionTests.test_delete_on_model_with_extra_fields_sets_pk_none delete.tests_llm.FastDeleteEarlyReturnRegressionTests.test_delete_returns_expected_counts_on_custom_pk_model delete.tests_llm.FastDeleteEarlyReturnRegressionTests.test_delete_with_transaction_context_sets_pk_none delete.tests_llm.FastDeleteEarlyReturnRegressionTests.test_multiple_dynamic_models_independent_deletes
coverage json -o coverage.json
: '>>>>> End Test Output'
