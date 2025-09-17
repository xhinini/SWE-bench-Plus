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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 backends.base.test_creation_llm.TestDeserializeInvokesConstraintChecks._make_cm backends.base.test_creation_llm.TestDeserializeInvokesConstraintChecks.test_check_constraints_called_for_circular_reference_payload backends.base.test_creation_llm.TestDeserializeInvokesConstraintChecks.test_check_constraints_called_for_empty_list_payload backends.base.test_creation_llm.TestDeserializeInvokesConstraintChecks.test_check_constraints_called_for_payload_with_newlines backends.base.test_creation_llm.TestDeserializeInvokesConstraintChecks.test_check_constraints_called_for_simple_payload backends.base.test_creation_llm.TestDeserializeInvokesConstraintChecks.test_check_constraints_called_multiple_times_on_multiple_invocations backends.base.test_creation_llm.TestDeserializeInvokesConstraintChecks.test_check_constraints_called_when_deserialize_returns_generator backends.base.test_creation_llm.TestDeserializeInvokesConstraintChecks.test_check_constraints_called_when_many_objects backends.base.test_creation_llm.TestDeserializeInvokesConstraintChecks.test_check_constraints_called_with_different_connection_alias backends.base.test_creation_llm.TestDeserializeInvokesConstraintChecks.test_constraint_context_entered_before_saves backends.base.test_creation_llm.TestDeserializeInvokesConstraintChecks.test_constraint_context_used_even_for_whitespace_payload
coverage json -o coverage.json
: '>>>>> End Test Output'
