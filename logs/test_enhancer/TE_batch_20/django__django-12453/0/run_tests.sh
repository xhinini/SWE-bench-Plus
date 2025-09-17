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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 backends.base.test_creation_llm.AdditionalDeserializeDbFromStringTests._get_pair_data_obj_then_ref backends.base.test_creation_llm.AdditionalDeserializeDbFromStringTests._get_pair_data_ref_then_obj backends.base.test_creation_llm.AdditionalDeserializeDbFromStringTests._get_two_pairs_mixed_order backends.base.test_creation_llm.AdditionalDeserializeDbFromStringTests.test_circular_reference_obj_then_ref backends.base.test_creation_llm.AdditionalDeserializeDbFromStringTests.test_circular_reference_ref_then_obj backends.base.test_creation_llm.AdditionalDeserializeDbFromStringTests.test_circular_reference_self_reference backends.base.test_creation_llm.AdditionalDeserializeDbFromStringTests.test_circular_reference_with_related_objects_populated backends.base.test_creation_llm.AdditionalDeserializeDbFromStringTests.test_constraint_checks_disabled_and_check_constraints_called backends.base.test_creation_llm.AdditionalDeserializeDbFromStringTests.test_deserialize_rolls_back_on_error_leaving_no_partial_objects backends.base.test_creation_llm.AdditionalDeserializeDbFromStringTests.test_deserialize_with_forward_references_in_long_list backends.base.test_creation_llm.AdditionalDeserializeDbFromStringTests.test_multiple_circular_pairs backends.base.test_creation_llm.AdditionalDeserializeDbFromStringTests.test_two_objects_cross_reference_each_other
coverage json -o coverage.json
: '>>>>> End Test Output'
