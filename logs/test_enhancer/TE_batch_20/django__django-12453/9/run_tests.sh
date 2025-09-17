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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 backends.base.test_creation_llm.TestDeserializeDbFromStringConstraintChecks.test_check_constraints_called_for_copy_connection backends.base.test_creation_llm.TestDeserializeDbFromStringConstraintChecks.test_check_constraints_called_on_default_connection backends.base.test_creation_llm.TestDeserializeDbFromStringConstraintChecks.test_check_constraints_called_once_with_empty_data backends.base.test_creation_llm.TestDeserializeDbFromStringConstraintChecks.test_check_constraints_called_with_large_empty_data backends.base.test_creation_llm.TestDeserializeDbFromStringConstraintChecks.test_check_constraints_called_with_multiline_empty_data backends.base.test_creation_llm.TestDeserializeDbFromStringConstraintChecks.test_check_constraints_called_with_whitespace_data backends.base.test_creation_llm.TestDeserializeDbFromStringConstraintChecks.test_constraint_checks_disabled_used_for_copy_connection backends.base.test_creation_llm.TestDeserializeDbFromStringConstraintChecks.test_constraint_checks_disabled_used_on_default_connection backends.base.test_creation_llm.TestDeserializeDbFromStringConstraintChecks.test_deserialize_calls_save_on_returned_objects_and_check_constraints_called backends.base.test_creation_llm.TestDeserializeDbFromStringConstraintChecks.test_deserialize_uses_constraint_checks_disabled_before_deserializing
coverage json -o coverage.json
: '>>>>> End Test Output'
