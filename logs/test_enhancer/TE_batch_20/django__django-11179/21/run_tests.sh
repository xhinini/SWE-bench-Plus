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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 delete.tests_llm.FastDeletePkRegressionTests._assert_deleted_and_pk_cleared delete.tests_llm.FastDeletePkRegressionTests.test_avatar_collector_delete_clears_pk delete.tests_llm.FastDeletePkRegressionTests.test_avatar_model_delete_clears_pk delete.tests_llm.FastDeletePkRegressionTests.test_m2mfrom_collector_delete_clears_pk delete.tests_llm.FastDeletePkRegressionTests.test_m2mfrom_model_delete_clears_pk delete.tests_llm.FastDeletePkRegressionTests.test_m2mto_collector_delete_clears_pk delete.tests_llm.FastDeletePkRegressionTests.test_m2mto_model_delete_clears_pk delete.tests_llm.FastDeletePkRegressionTests.test_m_collector_delete_clears_pk delete.tests_llm.FastDeletePkRegressionTests.test_m_model_delete_clears_pk delete.tests_llm.FastDeletePkRegressionTests.test_user_collector_delete_clears_pk delete.tests_llm.FastDeletePkRegressionTests.test_user_model_delete_clears_pk
coverage json -o coverage.json
: '>>>>> End Test Output'
