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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 backends.base.test_creation_llm.TestDeserializeCallsConstraintChecks._assert_constraints_called backends.base.test_creation_llm.TestDeserializeCallsConstraintChecks.test_constraints_called_child_before_parent backends.base.test_creation_llm.TestDeserializeCallsConstraintChecks.test_constraints_called_circular_reference backends.base.test_creation_llm.TestDeserializeCallsConstraintChecks.test_constraints_called_empty_list backends.base.test_creation_llm.TestDeserializeCallsConstraintChecks.test_constraints_called_many_relations backends.base.test_creation_llm.TestDeserializeCallsConstraintChecks.test_constraints_called_multiple_objects backends.base.test_creation_llm.TestDeserializeCallsConstraintChecks.test_constraints_called_non_sequential_pks backends.base.test_creation_llm.TestDeserializeCallsConstraintChecks.test_constraints_called_single_object backends.base.test_creation_llm.TestDeserializeCallsConstraintChecks.test_constraints_called_whitespace_only backends.base.test_creation_llm.TestDeserializeCallsConstraintChecks.test_constraints_called_with_extra_whitespace_and_newlines backends.base.test_creation_llm.TestDeserializeCallsConstraintChecks.test_constraints_called_with_unrelated_apps_present
coverage json -o coverage.json
: '>>>>> End Test Output'
