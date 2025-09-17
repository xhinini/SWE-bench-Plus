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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 backends.base.test_creation_llm.DummyCM.__enter__ backends.base.test_creation_llm.DummyCM.__exit__ backends.base.test_creation_llm.DummyCM.__init__ backends.base.test_creation_llm.TestDeserializeDbFromStringAdditional._make_atomic backends.base.test_creation_llm.TestDeserializeDbFromStringAdditional._make_constraint_cm backends.base.test_creation_llm.TestDeserializeDbFromStringAdditional.setUp backends.base.test_creation_llm.TestDeserializeDbFromStringAdditional.test_atomic_and_constraint_sequence backends.base.test_creation_llm.TestDeserializeDbFromStringAdditional.test_atomic_and_no_check_constraints_on_exception backends.base.test_creation_llm.TestDeserializeDbFromStringAdditional.test_atomic_used_in_module backends.base.test_creation_llm.TestDeserializeDbFromStringAdditional.test_check_constraints_called_even_when_no_objects backends.base.test_creation_llm.TestDeserializeDbFromStringAdditional.test_constraint_checks_disabled_called backends.base.test_creation_llm.TestDeserializeDbFromStringAdditional.test_constraint_cm_called_only_once_for_multiple_objects backends.base.test_creation_llm.TestDeserializeDbFromStringAdditional.test_each_deserialized_object_save_called backends.base.test_creation_llm.TestDeserializeDbFromStringAdditional.test_empty_string_is_handled_and_contexts_called backends.base.test_creation_llm.TestDeserializeDbFromStringAdditional.test_serializers_called_with_using_parameter
coverage json -o coverage.json
: '>>>>> End Test Output'
