#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 backends.sqlite.test_features_llm.BuildInstanceTests.test_multiple_fields_in_natural_key_using_relations backends.sqlite.test_features_llm.BuildInstanceTests.test_natural_key_accesses_related_object_attribute backends.sqlite.test_features_llm.BuildInstanceTests.test_natural_key_relies_on_related_field_value_set_by_Model_init backends.sqlite.test_features_llm.BuildInstanceTests.test_natural_key_uses__state_db backends.sqlite.test_features_llm.BuildInstanceTests.test_natural_key_uses_nested_related_object_and_state backends.sqlite.test_features_llm.BuildInstanceTests.test_natural_key_uses_state_and_related_field backends.sqlite.test_features_llm.BuildInstanceTests.test_related_field_missing_in_partial_instance_breaks_natural_key backends.sqlite.test_features_llm.FakeManager.__init__ backends.sqlite.test_features_llm.FakeManager.db_manager backends.sqlite.test_features_llm.FakeManager.get_by_natural_key backends.sqlite.test_features_llm.FakePK.__init__ backends.sqlite.test_features_llm.FakePK.to_python backends.sqlite.test_features_llm.make_meta backends.sqlite.test_features_llm.make_model_class
coverage json -o coverage.json
: '>>>>> End Test Output'
