#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 model_fields.tests_llm.FieldHashTests.test_hash_different_for_different_creation_counters model_fields.tests_llm.FieldHashTests.test_hash_equal_when_eq_true model_fields.tests_llm.FieldHashTests.test_hash_is_int model_fields.tests_llm.FieldHashTests.test_hash_same_after_deepcopy model_fields.tests_llm.FieldHashTests.test_hash_same_after_pickle_unpickle_attached model_fields.tests_llm.FieldHashTests.test_hash_same_after_pickle_unpickle_unattached model_fields.tests_llm.FieldHashTests.test_hash_same_after_shallow_copy model_fields.tests_llm.FieldHashTests.test_hash_unaffected_by_model_meta_mutation model_fields.tests_llm.FieldHashTests.test_hash_unchanged_on_contribute_to_class model_fields.tests_llm.FieldHashTests.test_hash_unchanged_when_setting_model_attribute_manually
coverage json -o coverage.json
: '>>>>> End Test Output'
