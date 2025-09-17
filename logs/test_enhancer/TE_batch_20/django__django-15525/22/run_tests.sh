#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 backends.sqlite.test_features_llm.BuildInstanceTests.test_db_manager_called_with_db backends.sqlite.test_features_llm.BuildInstanceTests.test_db_propagation_to_natural_key_simple backends.sqlite.test_features_llm.BuildInstanceTests.test_get_by_natural_key_does_not_exist_is_ignored backends.sqlite.test_features_llm.BuildInstanceTests.test_get_by_natural_key_sets_pk_with_to_python backends.sqlite.test_features_llm.BuildInstanceTests.test_multiple_calls_with_different_dbs_propagate_correctly backends.sqlite.test_features_llm.BuildInstanceTests.test_natural_key_multiple_components_including_relation backends.sqlite.test_features_llm.BuildInstanceTests.test_natural_key_with_additional_field backends.sqlite.test_features_llm.BuildInstanceTests.test_no_get_by_natural_key_method_skipped backends.sqlite.test_features_llm.BuildInstanceTests.test_no_lookup_when_pk_present backends.sqlite.test_features_llm.BuildInstanceTests.test_relation_attribute_used_in_natural_key backends.sqlite.test_features_llm.make_model_class
coverage json -o coverage.json
: '>>>>> End Test Output'
