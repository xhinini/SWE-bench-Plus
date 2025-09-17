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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 delete.tests_llm.FastDeletePkRegressionTests._skip_unless_fast_deletable delete.tests_llm.FastDeletePkRegressionTests.test_avatar_instance_delete_sets_pk_none_when_unreferenced delete.tests_llm.FastDeletePkRegressionTests.test_child_model_simple_instance_delete_sets_pk_none_when_fast delete.tests_llm.FastDeletePkRegressionTests.test_m_model_instance_delete_sets_pk_none delete.tests_llm.FastDeletePkRegressionTests.test_model_with_simple_relation_delete_sets_pk_none delete.tests_llm.FastDeletePkRegressionTests.test_parent_model_instance_delete_sets_pk_none_when_fast
coverage json -o coverage.json
: '>>>>> End Test Output'
