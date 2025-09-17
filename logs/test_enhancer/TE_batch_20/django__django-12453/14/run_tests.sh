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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 backends.base.test_creation_llm.TestDeserializeDbFromStringRegression.setUp backends.base.test_creation_llm.TestDeserializeDbFromStringRegression.test_check_constraints_and_context_manager_are_called backends.base.test_creation_llm.TestDeserializeDbFromStringRegression.test_constraint_checks_disabled_context_entered backends.base.test_creation_llm.TestDeserializeDbFromStringRegression.test_deserialize_failure_rolls_back_all_changes backends.base.test_creation_llm.TestDeserializeDbFromStringRegression.test_deserialize_preserves_relations_after_restore backends.base.test_creation_llm.TestDeserializeDbFromStringRegression.test_deserialize_with_missing_foreign_key_raises_integrity_error backends.base.test_creation_llm.TestDeserializeDbFromStringRegression.test_serialize_then_deserialize_restores_data
coverage json -o coverage.json
: '>>>>> End Test Output'
