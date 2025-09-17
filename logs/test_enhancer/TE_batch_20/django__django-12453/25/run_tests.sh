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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 backends.base.test_creation_llm.FakeCM.__enter__ backends.base.test_creation_llm.FakeCM.__exit__ backends.base.test_creation_llm.FakeCM.__init__ backends.base.test_creation_llm.FakeDeserialized.__init__ backends.base.test_creation_llm.FakeDeserialized.save backends.base.test_creation_llm.TestDeserializeDbFromStringRegression.test_check_constraints_called_after_saves backends.base.test_creation_llm.TestDeserializeDbFromStringRegression.test_check_constraints_exception_propagates backends.base.test_creation_llm.TestDeserializeDbFromStringRegression.test_constraint_checks_disabled_and_check_constraints_called_for_empty_data backends.base.test_creation_llm.TestDeserializeDbFromStringRegression.test_constraint_checks_disabled_context_exited_on_deserialize_exception backends.base.test_creation_llm.TestDeserializeDbFromStringRegression.test_constraint_context_used_on_different_alias_runs_check_constraints backends.base.test_creation_llm.TestDeserializeDbFromStringRegression.test_deserialize_calls_save_on_each_deserialized_object backends.base.test_creation_llm.TestDeserializeDbFromStringRegression.test_multiple_calls_use_context_each_time backends.base.test_creation_llm.TestDeserializeDbFromStringRegression.test_objects_saved_within_constraint_checks_disabled_context_and_ordered backends.base.test_creation_llm.TestDeserializeDbFromStringRegression.test_serializer_receives_StringIO_and_using_arguments
coverage json -o coverage.json
: '>>>>> End Test Output'
