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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 backends.base.test_creation_llm.TestDeserializeDbFromStringRegression._make_cm backends.base.test_creation_llm.TestDeserializeDbFromStringRegression.test_check_constraints_called_after_multiple_saves backends.base.test_creation_llm.TestDeserializeDbFromStringRegression.test_check_constraints_called_exactly_once_even_with_many_objects backends.base.test_creation_llm.TestDeserializeDbFromStringRegression.test_check_constraints_called_with_empty_deserialization backends.base.test_creation_llm.TestDeserializeDbFromStringRegression.test_constraint_context_entered_and_exited backends.base.test_creation_llm.TestDeserializeDbFromStringRegression.test_deserialize_accepts_generator_from_serializer backends.base.test_creation_llm.TestDeserializeDbFromStringRegression.test_deserializer_called_with_provided_data_stream backends.base.test_creation_llm.TestDeserializeDbFromStringRegression.test_multiple_saves_and_single_check_constraints_call backends.base.test_creation_llm.TestDeserializeDbFromStringRegression.test_ordering_of_save_and_check_with_no_objects backends.base.test_creation_llm.TestDeserializeDbFromStringRegression.test_serializers_called_with_json_and_using backends.base.test_creation_llm.TestDeserializeDbFromStringRegression.test_stream_is_stringio_passed_to_serializer
coverage json -o coverage.json
: '>>>>> End Test Output'
