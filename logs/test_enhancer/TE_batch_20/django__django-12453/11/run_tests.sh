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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 backends.base.test_creation_llm.TestDeserializeConstraintChecks.test_check_constraints_called_default_connection backends.base.test_creation_llm.TestDeserializeConstraintChecks.test_check_constraints_called_exactly_once backends.base.test_creation_llm.TestDeserializeConstraintChecks.test_check_constraints_called_nondefault_connection backends.base.test_creation_llm.TestDeserializeConstraintChecks.test_constraint_checks_disabled_entered_before_any_model_save backends.base.test_creation_llm.TestDeserializeConstraintChecks.test_constraint_checks_disabled_used_default_connection backends.base.test_creation_llm.TestDeserializeConstraintChecks.test_constraint_checks_disabled_used_nondefault_connection backends.base.test_creation_llm.TestDeserializeConstraintChecks.test_deserialize_calls_constraint_checks_with_circular_data backends.base.test_creation_llm.TestDeserializeConstraintChecks.test_deserialize_calls_constraint_checks_with_multiple_objects backends.base.test_creation_llm.TestDeserializeConstraintChecks.test_empty_payload_still_calls_check_constraints backends.base.test_creation_llm.TestDeserializeConstraintChecks.test_serialize_deserialize_roundtrip_triggers_check_constraints backends.base.test_creation_llm.get_connection_copy
coverage json -o coverage.json
: '>>>>> End Test Output'
