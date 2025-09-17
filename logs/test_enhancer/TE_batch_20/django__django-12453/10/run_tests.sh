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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 backends.base.test_creation_llm.DummyCM.__enter__ backends.base.test_creation_llm.DummyCM.__exit__ backends.base.test_creation_llm.DummyCM.__init__ backends.base.test_creation_llm.TestDeserializeDbRegressions.setUp backends.base.test_creation_llm.TestDeserializeDbRegressions.test_atomic_and_constraint_combination_for_simple_object backends.base.test_creation_llm.TestDeserializeDbRegressions.test_atomic_called_from_creation_module backends.base.test_creation_llm.TestDeserializeDbRegressions.test_check_constraints_called_after_saving_objects_in_order backends.base.test_creation_llm.TestDeserializeDbRegressions.test_constraint_checks_disabled_called_for_circular_reference_data backends.base.test_creation_llm.TestDeserializeDbRegressions.test_constraint_checks_disabled_called_on_empty_data backends.base.test_creation_llm.TestDeserializeDbRegressions.test_constraint_checks_disabled_called_on_non_empty_data backends.base.test_creation_llm.TestDeserializeDbRegressions.test_constraint_context_exit_on_exception_during_save backends.base.test_creation_llm.TestDeserializeDbRegressions.test_constraint_context_manager_enter_and_exit_even_with_multiple_objects backends.base.test_creation_llm.TestDeserializeDbRegressions.test_deserialize_passes_using_argument_to_serializers
coverage json -o coverage.json
: '>>>>> End Test Output'
