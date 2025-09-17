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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 backends.base.test_creation_llm.AdditionalDeserializeTests.test_check_constraints_called_even_if_deserialize_generator_consumes_stream backends.base.test_creation_llm.AdditionalDeserializeTests.test_constraint_checks_disabled_and_check_constraints_called_default_connection backends.base.test_creation_llm.AdditionalDeserializeTests.test_constraint_checks_disabled_called_once_for_many_objects backends.base.test_creation_llm.AdditionalDeserializeTests.test_creation_instance_uses_its_own_connection_methods backends.base.test_creation_llm.AdditionalDeserializeTests.test_deserialize_calls_constraint_checks_disabled_for_creation_instance backends.base.test_creation_llm.AdditionalDeserializeTests.test_deserialize_passes_using_argument_to_serializers backends.base.test_creation_llm.AdditionalDeserializeTests.test_deserialize_saves_objects_in_order_and_calls_check_after_exit backends.base.test_creation_llm.AdditionalDeserializeTests.test_empty_serialized_input_still_calls_check_constraints backends.base.test_creation_llm.AdditionalDeserializeTests.test_sequence_of_events_when_saves_and_checks_are_called backends.base.test_creation_llm.DummyCM.__enter__ backends.base.test_creation_llm.DummyCM.__exit__ backends.base.test_creation_llm.DummyCM.__init__
coverage json -o coverage.json
: '>>>>> End Test Output'
