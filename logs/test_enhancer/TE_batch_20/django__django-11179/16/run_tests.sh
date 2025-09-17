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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 delete.tests_llm.RegressionFastDeletePkTests.test_char_pk_instance_delete_sets_pk_none delete.tests_llm.RegressionFastDeletePkTests.test_custom_db_column_pk_sets_attribute_to_none delete.tests_llm.RegressionFastDeletePkTests.test_delete_after_bulk_creation_single_instance_pk_none delete.tests_llm.RegressionFastDeletePkTests.test_multiple_instances_delete_single_one_others_unchanged delete.tests_llm.RegressionFastDeletePkTests.test_repeated_delete_calls_first_clears_pk_and_second_is_noop delete.tests_llm.RegressionFastDeletePkTests.test_slug_pk_attname_set_to_none delete.tests_llm.RegressionFastDeletePkTests.test_uuid_pk_instance_delete_sets_pk_none
coverage json -o coverage.json
: '>>>>> End Test Output'
