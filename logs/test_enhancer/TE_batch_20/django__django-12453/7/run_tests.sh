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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 backends.base.test_creation_llm.DeserializeConstraintTests._make_cm_and_hooks backends.base.test_creation_llm.DeserializeConstraintTests.test_check_constraints_called_after_exit backends.base.test_creation_llm.DeserializeConstraintTests.test_constraint_context_and_check_constraints_called_single_object backends.base.test_creation_llm.DeserializeConstraintTests.test_deserialize_on_custom_connection_uses_its_methods backends.base.test_creation_llm.DeserializeConstraintTests.test_deserialize_passes_using_to_serializers backends.base.test_creation_llm.DeserializeConstraintTests.test_deserialize_works_with_generator_from_serializers backends.base.test_creation_llm.DeserializeConstraintTests.test_multiple_objects_order backends.base.test_creation_llm.DeserializeConstraintTests.test_no_objects_still_calls_context_and_check_constraints backends.base.test_creation_llm.DeserializeConstraintTests.test_order_with_mixed_iterator_and_list backends.base.test_creation_llm.DeserializeConstraintTests.test_save_called_for_each_deserialized_object
coverage json -o coverage.json
: '>>>>> End Test Output'
