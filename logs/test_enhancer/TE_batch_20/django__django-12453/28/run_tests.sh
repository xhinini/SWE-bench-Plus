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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 backends.base.test_creation_llm.TestDeserializeDbFromStringAtomicAndConstraints._patch_deserialize_and_run backends.base.test_creation_llm.TestDeserializeDbFromStringAtomicAndConstraints.test_atomic_entered_before_saves backends.base.test_creation_llm.TestDeserializeDbFromStringAtomicAndConstraints.test_atomic_is_used_even_for_empty_data backends.base.test_creation_llm.TestDeserializeDbFromStringAtomicAndConstraints.test_calls_check_constraints_after_successful_deserialize backends.base.test_creation_llm.TestDeserializeDbFromStringAtomicAndConstraints.test_check_constraints_called_with_multiple_objects backends.base.test_creation_llm.TestDeserializeDbFromStringAtomicAndConstraints.test_constraint_context_entered_even_for_empty_data backends.base.test_creation_llm.TestDeserializeDbFromStringAtomicAndConstraints.test_constraint_context_exited_on_exception backends.base.test_creation_llm.TestDeserializeDbFromStringAtomicAndConstraints.test_constraint_wraps_multiple_saves backends.base.test_creation_llm.TestDeserializeDbFromStringAtomicAndConstraints.test_uses_constraint_checks_disabled backends.base.test_creation_llm.TestDeserializeDbFromStringAtomicAndConstraints.test_uses_module_atomic_with_using_arg backends.base.test_creation_llm._FakeCM.__enter__ backends.base.test_creation_llm._FakeCM.__exit__ backends.base.test_creation_llm._FakeCM.__init__
coverage json -o coverage.json
: '>>>>> End Test Output'
