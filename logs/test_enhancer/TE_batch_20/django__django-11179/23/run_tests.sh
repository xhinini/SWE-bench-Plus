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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 delete.tests_llm.CollectorOptimizedDeleteTests.test_collector_single_delete_avatar_pk_cleared delete.tests_llm.CollectorOptimizedDeleteTests.test_collector_single_delete_child_pk_cleared delete.tests_llm.CollectorOptimizedDeleteTests.test_collector_single_delete_hiddenuser_pk_cleared delete.tests_llm.CollectorOptimizedDeleteTests.test_collector_single_delete_m2mto_pk_cleared delete.tests_llm.CollectorOptimizedDeleteTests.test_collector_single_delete_nullable_true_pk_cleared delete.tests_llm.CollectorOptimizedDeleteTests.test_collector_single_delete_parent_pk_cleared delete.tests_llm.CollectorOptimizedDeleteTests.test_collector_single_delete_r_pk_cleared delete.tests_llm.CollectorOptimizedDeleteTests.test_collector_single_delete_reverse_dependency_pk_cleared delete.tests_llm.CollectorOptimizedDeleteTests.test_collector_single_delete_user_pk_cleared delete.tests_llm.CollectorOptimizedDeleteTests.test_collector_single_delete_with_keep_parents_pk_cleared
coverage json -o coverage.json
: '>>>>> End Test Output'
