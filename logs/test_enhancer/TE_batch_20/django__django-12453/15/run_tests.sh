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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 backends.base.test_creation_llm.TestDeserializeConstraintHooks._make_cm backends.base.test_creation_llm.TestDeserializeConstraintHooks.test_check_not_called_on_save_error backends.base.test_creation_llm.TestDeserializeConstraintHooks.test_check_not_called_on_serialize_error backends.base.test_creation_llm.TestDeserializeConstraintHooks.test_constraint_and_check_called_with_empty backends.base.test_creation_llm.TestDeserializeConstraintHooks.test_constraint_and_check_called_with_objects_generator backends.base.test_creation_llm.TestDeserializeConstraintHooks.test_constraint_and_check_called_with_objects_list backends.base.test_creation_llm.TestDeserializeConstraintHooks.test_constraint_enter_and_exit_called backends.base.test_creation_llm.TestDeserializeConstraintHooks.test_constraint_manager_used_when_check_constraints_raises backends.base.test_creation_llm.TestDeserializeConstraintHooks.test_deserialize_called_with_using_parameter backends.base.test_creation_llm.TestDeserializeConstraintHooks.test_multiple_calls_check_called_each_time
coverage json -o coverage.json
: '>>>>> End Test Output'
