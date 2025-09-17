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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 backends.base.test_creation_llm.TestDeserializeDbConstraintHandling._make_cm_toggle backends.base.test_creation_llm.TestDeserializeDbConstraintHandling.test_check_constraints_called backends.base.test_creation_llm.TestDeserializeDbConstraintHandling.test_check_constraints_called_after_save backends.base.test_creation_llm.TestDeserializeDbConstraintHandling.test_check_constraints_called_on_connection_copy backends.base.test_creation_llm.TestDeserializeDbConstraintHandling.test_constraint_checks_disabled_called backends.base.test_creation_llm.TestDeserializeDbConstraintHandling.test_constraint_context_exit_on_exception backends.base.test_creation_llm.TestDeserializeDbConstraintHandling.test_constraint_disabled_before_save backends.base.test_creation_llm.TestDeserializeDbConstraintHandling.test_constraint_manager_used_with_whitespace_data backends.base.test_creation_llm.TestDeserializeDbConstraintHandling.test_deserialize_uses_module_level_atomic backends.base.test_creation_llm.TestDeserializeDbConstraintHandling.test_empty_data_still_calls_constraint_and_check backends.base.test_creation_llm.TestDeserializeDbConstraintHandling.test_multiple_objects_save_order_with_checks
coverage json -o coverage.json
: '>>>>> End Test Output'
