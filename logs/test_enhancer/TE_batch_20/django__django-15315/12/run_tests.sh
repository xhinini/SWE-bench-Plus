#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 model_fields.tests_llm.FieldHashRegressionTests.test_hash_equal_to_meta_get_field_for_bound_field model_fields.tests_llm.FieldHashRegressionTests.test_hash_unchanged_when_field_attached_via_class_definition model_fields.tests_llm.FieldHashRegressionTests.test_pickle_bound_field_returns_same_object_and_hash model_fields.tests_llm.FieldHashRegressionTests.test_pickling_container_of_bound_field_preserves_keys model_fields.tests_llm.FieldHashRegressionTests.test_set_membership_preserved_after_class_bind
coverage json -o coverage.json
: '>>>>> End Test Output'
