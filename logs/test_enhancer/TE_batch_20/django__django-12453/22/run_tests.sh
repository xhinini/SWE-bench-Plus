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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 backends.base.test_creation_llm.DeserializeDbFromStringRegressionTests.test_atomic_context_manager_is_used_for_deserialize backends.base.test_creation_llm.DeserializeDbFromStringRegressionTests.test_atomic_used_even_with_nonempty_payload backends.base.test_creation_llm.DeserializeDbFromStringRegressionTests.test_check_constraints_called_after_deserialize backends.base.test_creation_llm.DeserializeDbFromStringRegressionTests.test_circular_reference_deserialization_uses_constraint_disable_and_atomic backends.base.test_creation_llm.DeserializeDbFromStringRegressionTests.test_constraint_checks_disabled_called_each_time_deserialize_invoked backends.base.test_creation_llm.DeserializeDbFromStringRegressionTests.test_constraint_checks_disabled_context_manager_is_used backends.base.test_creation_llm.DeserializeDbFromStringRegressionTests.test_deserialize_saves_objects_and_calls_check_constraints backends.base.test_creation_llm.DeserializeDbFromStringRegressionTests.test_order_of_operations_constraint_disable_then_check_constraints backends.base.test_creation_llm.DummyCM.__enter__ backends.base.test_creation_llm.DummyCM.__exit__ backends.base.test_creation_llm.DummyCM.__init__
coverage json -o coverage.json
: '>>>>> End Test Output'
