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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 delete.tests_llm.AdditionalDeletionPkTests.test_avatar_delete_single_instance_sets_pk_none delete.tests_llm.AdditionalDeletionPkTests.test_child_delete_inheritance_sets_pk_none delete.tests_llm.AdditionalDeletionPkTests.test_collector_collect_then_delete_sets_pk_none delete.tests_llm.AdditionalDeletionPkTests.test_collector_fast_delete_single_model_returns_counts_and_sets_pk delete.tests_llm.AdditionalDeletionPkTests.test_delete_with_m2m_related_cleanup_and_pk_none delete.tests_llm.AdditionalDeletionPkTests.test_deleting_one_of_many_does_not_affect_other_instances delete.tests_llm.AdditionalDeletionPkTests.test_keep_parents_child_delete_sets_pk_none_but_parent_remains delete.tests_llm.AdditionalDeletionPkTests.test_model_delete_returns_counts_and_sets_pk_none_user delete.tests_llm.AdditionalDeletionPkTests.test_parent_delete_cascades_and_child_pk_becomes_none delete.tests_llm.AdditionalDeletionPkTests.test_user_delete_sets_pk_none
coverage json -o coverage.json
: '>>>>> End Test Output'
