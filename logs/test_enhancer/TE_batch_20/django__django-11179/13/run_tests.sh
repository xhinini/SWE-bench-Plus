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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 delete.tests_llm.RegressionDeletionTests._create_model delete.tests_llm.RegressionDeletionTests._delete_model delete.tests_llm.RegressionDeletionTests.test_custom_field_name_pk_delete_sets_pk_none delete.tests_llm.RegressionDeletionTests.test_dynamic_bigautofield_pk_delete_sets_pk_none delete.tests_llm.RegressionDeletionTests.test_dynamic_char_pk_delete_sets_pk_none delete.tests_llm.RegressionDeletionTests.test_dynamic_default_auto_pk_delete_sets_pk_none delete.tests_llm.RegressionDeletionTests.test_dynamic_uuid_pk_delete_sets_pk_none delete.tests_llm.RegressionDeletionTests.test_inherited_model_delete_sets_pk_none delete.tests_llm.RegressionDeletionTests.test_multiple_sequential_single_deletes_clear_pk delete.tests_llm.RegressionDeletionTests.test_proxy_model_delete_sets_pk_none
coverage json -o coverage.json
: '>>>>> End Test Output'
