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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 backends.base.test_creation_llm.TestDeserializeDbFromStringConstraintBehavior.test_both_methods_called_for_multiple_objects backends.base.test_creation_llm.TestDeserializeDbFromStringConstraintBehavior.test_check_constraints_called_only_once_even_with_many_objects backends.base.test_creation_llm.TestDeserializeDbFromStringConstraintBehavior.test_check_constraints_called_single_object backends.base.test_creation_llm.TestDeserializeDbFromStringConstraintBehavior.test_constraint_checks_disabled_called_single_object backends.base.test_creation_llm.TestDeserializeDbFromStringConstraintBehavior.test_constraint_entered_before_each_save backends.base.test_creation_llm.TestDeserializeDbFromStringConstraintBehavior.test_empty_iterable_still_calls_context_and_check_constraints backends.base.test_creation_llm.TestDeserializeDbFromStringConstraintBehavior.test_generator_deserialize_consumed_and_context_exited backends.base.test_creation_llm.TestDeserializeDbFromStringConstraintBehavior.test_objects_saved_in_order backends.base.test_creation_llm._make_cm_tracker
coverage json -o coverage.json
: '>>>>> End Test Output'
