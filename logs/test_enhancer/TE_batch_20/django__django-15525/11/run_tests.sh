#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 backends.sqlite.test_features_llm.BuildInstanceTests.test_converts_pk_using_to_python backends.sqlite.test_features_llm.BuildInstanceTests.test_handles_db_none backends.sqlite.test_features_llm.BuildInstanceTests.test_handles_string_pk_conversion backends.sqlite.test_features_llm.BuildInstanceTests.test_multiple_components_natural_key backends.sqlite.test_features_llm.BuildInstanceTests.test_multiple_relational_fields_in_data backends.sqlite.test_features_llm.BuildInstanceTests.test_nested_related_object_natural_key backends.sqlite.test_features_llm.BuildInstanceTests.test_sets_pk_from_natural_key_with_related_object backends.sqlite.test_features_llm.BuildInstanceTests.test_uses_provided_db_in_db_manager_call backends.sqlite.test_features_llm.FakeField.__init__ backends.sqlite.test_features_llm.FakeManager.__init__ backends.sqlite.test_features_llm.FakeManager.db_manager backends.sqlite.test_features_llm.FakeManager.get_by_natural_key backends.sqlite.test_features_llm.FakeMeta.__init__ backends.sqlite.test_features_llm.FakeMeta.get_field backends.sqlite.test_features_llm.FakeModel.__init__ backends.sqlite.test_features_llm.FakeModel.__repr__ backends.sqlite.test_features_llm.PKDescriptor.__init__ backends.sqlite.test_features_llm.[] (backends.sqlite.test_features_llm.FakeModel) backends.sqlite.test_features_llm.make_model_class
coverage json -o coverage.json
: '>>>>> End Test Output'
