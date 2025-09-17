#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 model_fields.tests_llm.FieldHashRegressionTests.test_booleanfield_hash_immutable_after_attach model_fields.tests_llm.FieldHashRegressionTests.test_charfield_hash_immutable_after_attach model_fields.tests_llm.FieldHashRegressionTests.test_contribute_to_class_does_not_change_hash model_fields.tests_llm.FieldHashRegressionTests.test_datefield_hash_immutable_after_attach model_fields.tests_llm.FieldHashRegressionTests.test_decimalfield_hash_immutable_after_attach model_fields.tests_llm.FieldHashRegressionTests.test_fields_with_same_creation_counter_have_same_hash_regardless_of_model model_fields.tests_llm.FieldHashRegressionTests.test_hash_stability_after_copy model_fields.tests_llm.FieldHashRegressionTests.test_integerfield_hash_immutable_after_attach
coverage json -o coverage.json
: '>>>>> End Test Output'
