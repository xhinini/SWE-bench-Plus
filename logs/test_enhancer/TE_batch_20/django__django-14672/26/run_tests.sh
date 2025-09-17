#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 invalid_models_tests.test_models_llm.ManyToManyRelThroughFieldsTests.test_empty_list_and_empty_tuple_map_to_same_dict_key invalid_models_tests.test_models_llm.ManyToManyRelThroughFieldsTests.test_empty_list_equals_empty_tuple invalid_models_tests.test_models_llm.ManyToManyRelThroughFieldsTests.test_identity_component_hashable_when_empty_list invalid_models_tests.test_models_llm.ManyToManyRelThroughFieldsTests.test_identity_through_fields_empty_list_is_empty_tuple invalid_models_tests.test_models_llm.ManyToManyRelThroughFieldsTests.test_two_relations_with_empty_list_instances_are_equal invalid_models_tests.test_models_llm.make_rel
coverage json -o coverage.json
: '>>>>> End Test Output'
