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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 delete.tests_llm.CollectorDeleteRegressionTests.test_collector_delete_add_avatar_clears_pk delete.tests_llm.CollectorDeleteRegressionTests.test_collector_delete_add_simple_model_M_clears_pk delete.tests_llm.CollectorDeleteRegressionTests.test_collector_delete_add_then_direct_manipulation_clears_pk delete.tests_llm.CollectorDeleteRegressionTests.test_collector_delete_add_user_clears_pk delete.tests_llm.CollectorDeleteRegressionTests.test_collector_delete_direct_avatar_clears_pk delete.tests_llm.CollectorDeleteRegressionTests.test_collector_delete_direct_multiple_model_types_individual_clear delete.tests_llm.CollectorDeleteRegressionTests.test_collector_delete_direct_repeated_calls_clear_each_instance delete.tests_llm.CollectorDeleteRegressionTests.test_collector_delete_direct_simple_model_M_clears_pk delete.tests_llm.CollectorDeleteRegressionTests.test_collector_delete_direct_user_clears_pk delete.tests_llm.CollectorDeleteRegressionTests.test_collector_delete_with_pre_delete_listener_still_clears_pk
coverage json -o coverage.json
: '>>>>> End Test Output'
