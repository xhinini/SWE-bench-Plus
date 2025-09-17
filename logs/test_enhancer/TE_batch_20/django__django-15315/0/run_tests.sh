#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 model_fields.tests_llm.FieldHashRegressionTests.test_dict_key_survives_model_attach_charfield model_fields.tests_llm.FieldHashRegressionTests.test_dict_key_survives_model_attach_integerfield model_fields.tests_llm.FieldHashRegressionTests.test_hash_consistent_with_copy_after_attach model_fields.tests_llm.FieldHashRegressionTests.test_set_membership_survives_model_attach_auto_created_field model_fields.tests_llm.FieldHashRegressionTests.test_set_membership_survives_model_attach_charfield model_fields.tests_llm.FieldHashRegressionTests.test_set_membership_survives_model_attach_integerfield
coverage json -o coverage.json
: '>>>>> End Test Output'
