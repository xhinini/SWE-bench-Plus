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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 backends.base.test_creation_llm.DummyCM.__enter__ backends.base.test_creation_llm.DummyCM.__exit__ backends.base.test_creation_llm.DummyCM.__init__ backends.base.test_creation_llm.DummyObj.__init__ backends.base.test_creation_llm.DummyObj.save backends.base.test_creation_llm.TestDeserializeDbFromStringAdditional.test_atomic_symbol_from_module_used backends.base.test_creation_llm.TestDeserializeDbFromStringAdditional.test_check_constraints_called_on_circular_reference backends.base.test_creation_llm.TestDeserializeDbFromStringAdditional.test_check_constraints_called_on_empty_data backends.base.test_creation_llm.TestDeserializeDbFromStringAdditional.test_check_constraints_called_on_single_object backends.base.test_creation_llm.TestDeserializeDbFromStringAdditional.test_constraint_context_manager_enter_and_exit backends.base.test_creation_llm.TestDeserializeDbFromStringAdditional.test_constraint_disabled_called_before_save backends.base.test_creation_llm.TestDeserializeDbFromStringAdditional.test_deserialize_receives_using_argument_and_checks_constraints backends.base.test_creation_llm.TestDeserializeDbFromStringAdditional.test_multiple_objects_check_constraints_called backends.base.test_creation_llm.TestDeserializeDbFromStringAdditional.test_whitespace_only_input_still_invokes_constraints
coverage json -o coverage.json
: '>>>>> End Test Output'
