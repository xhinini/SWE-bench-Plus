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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 backends.base.test_creation_llm.TestDeserializeConstraintHandling._make_cm backends.base.test_creation_llm.TestDeserializeConstraintHandling.test_check_constraints_called_once_for_single_call backends.base.test_creation_llm.TestDeserializeConstraintHandling.test_check_constraints_called_twice_on_two_calls backends.base.test_creation_llm.TestDeserializeConstraintHandling.test_constraint_and_check_called_circular_reference backends.base.test_creation_llm.TestDeserializeConstraintHandling.test_constraint_and_check_called_empty_list backends.base.test_creation_llm.TestDeserializeConstraintHandling.test_constraint_and_check_called_reverse_order backends.base.test_creation_llm.TestDeserializeConstraintHandling.test_constraint_and_check_called_with_whitespace_data backends.base.test_creation_llm.TestDeserializeConstraintHandling.test_constraint_context_and_check_called_for_multiple_objects backends.base.test_creation_llm.TestDeserializeConstraintHandling.test_constraint_context_called_when_serialized_string_from_serialize_db_to_string backends.base.test_creation_llm.TestDeserializeConstraintHandling.test_constraint_context_enter_and_exit_called
coverage json -o coverage.json
: '>>>>> End Test Output'
