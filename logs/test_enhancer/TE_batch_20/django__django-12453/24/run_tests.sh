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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 backends.base.test_creation_llm.TestDeserializeConstraintChecks._cm_factory backends.base.test_creation_llm.TestDeserializeConstraintChecks.test_circular_data_uses_constraint_context_and_checks backends.base.test_creation_llm.TestDeserializeConstraintChecks.test_constraint_context_and_check_constraints_called_on_malformed_json_raises backends.base.test_creation_llm.TestDeserializeConstraintChecks.test_constraint_context_called_even_if_deserialize_iterates_zero backends.base.test_creation_llm.TestDeserializeConstraintChecks.test_constraint_context_called_multiple_times_in_repeated_calls backends.base.test_creation_llm.TestDeserializeConstraintChecks.test_empty_data_uses_constraint_context_and_checks backends.base.test_creation_llm.TestDeserializeConstraintChecks.test_multi_object_data_uses_constraint_context_and_checks backends.base.test_creation_llm.TestDeserializeConstraintChecks.test_ordering_when_objects_present backends.base.test_creation_llm.TestDeserializeConstraintChecks.test_simple_data_uses_constraint_context_and_checks backends.base.test_creation_llm.TestDeserializeConstraintChecks.test_whitespace_json_uses_constraint_context_and_checks
coverage json -o coverage.json
: '>>>>> End Test Output'
