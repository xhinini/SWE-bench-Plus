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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 delete.tests_llm.CollectorDeleteRegressionTests.test_collector_delete_inherited_model_clears_pk delete.tests_llm.CollectorDeleteRegressionTests.test_collector_delete_multiple_instances_clears_all_pks delete.tests_llm.CollectorDeleteRegressionTests.test_collector_delete_resets_pk_when_pre_delete_listeners_present delete.tests_llm.CollectorDeleteRegressionTests.test_collector_delete_single_avatar_clears_pk delete.tests_llm.CollectorDeleteRegressionTests.test_collector_delete_single_parent_clears_pk delete.tests_llm.CollectorDeleteRegressionTests.test_collector_delete_single_r_clears_pk delete.tests_llm.CollectorDeleteRegressionTests.test_collector_delete_single_rchild_clears_pk delete.tests_llm.CollectorDeleteRegressionTests.test_collector_delete_single_user_clears_pk delete.tests_llm.CollectorDeleteRegressionTests.test_collector_delete_with_field_update_scheduled_clears_pk
coverage json -o coverage.json
: '>>>>> End Test Output'
