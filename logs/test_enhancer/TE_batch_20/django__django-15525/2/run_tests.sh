#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 backends.sqlite.test_features_llm.BuildInstanceTests.test_attname_variant_author_id_sets_pk backends.sqlite.test_features_llm.BuildInstanceTests.test_db_forwarded_to_manager_db_manager backends.sqlite.test_features_llm.BuildInstanceTests.test_multiple_fields_including_relation backends.sqlite.test_features_llm.BuildInstanceTests.test_natural_key_accessing_nested_relation_attribute backends.sqlite.test_features_llm.BuildInstanceTests.test_natural_key_combines_relation_and_state_db backends.sqlite.test_features_llm.BuildInstanceTests.test_natural_key_requires_state_db_to_be_set backends.sqlite.test_features_llm.BuildInstanceTests.test_natural_key_using_relational_attribute_sets_pk backends.sqlite.test_features_llm.BuildInstanceTests.test_natural_key_when_multiple_serialized_fields_present backends.sqlite.test_features_llm.BuildInstanceTests.test_natural_key_with_various_field_names backends.sqlite.test_features_llm.BuildInstanceTests.test_pk_to_python_conversion_occurs backends.sqlite.test_features_llm.make_model
coverage json -o coverage.json
: '>>>>> End Test Output'
