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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 backends.base.test_creation_llm.TestDeserializeDbConstraintManagement._make_fake_obj backends.base.test_creation_llm.TestDeserializeDbConstraintManagement.test_check_constraints_called backends.base.test_creation_llm.TestDeserializeDbConstraintManagement.test_check_constraints_called_once_with_multiple_objects backends.base.test_creation_llm.TestDeserializeDbConstraintManagement.test_constraint_checks_disabled_enter_called backends.base.test_creation_llm.TestDeserializeDbConstraintManagement.test_constraint_checks_disabled_exit_called backends.base.test_creation_llm.TestDeserializeDbConstraintManagement.test_context_enter_before_any_save_order backends.base.test_creation_llm.TestDeserializeDbConstraintManagement.test_exit_before_check_constraints_order backends.base.test_creation_llm.TestDeserializeDbConstraintManagement.test_module_level_atomic_called backends.base.test_creation_llm.TestDeserializeDbConstraintManagement.test_multiple_objects_all_saved_and_checks_called_once backends.base.test_creation_llm.TestDeserializeDbConstraintManagement.test_no_objects_still_calls_constraint_manager_and_check_constraints backends.base.test_creation_llm.TestDeserializeDbConstraintManagement.test_save_called_inside_constraint_disabled_context
coverage json -o coverage.json
: '>>>>> End Test Output'
