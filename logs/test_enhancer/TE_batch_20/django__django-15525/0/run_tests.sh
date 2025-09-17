#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 backends.sqlite.test_features_llm.BuildInstanceTests.test_applies_pk_to_python_conversion backends.sqlite.test_features_llm.BuildInstanceTests.test_handles_does_not_exist_from_manager backends.sqlite.test_features_llm.BuildInstanceTests.test_multiple_different_db_names backends.sqlite.test_features_llm.BuildInstanceTests.test_natural_key_can_use_instance_attributes backends.sqlite.test_features_llm.BuildInstanceTests.test_returned_instance_fields_populated_from_data backends.sqlite.test_features_llm.BuildInstanceTests.test_sets_state_db_for_natural_key_resolution backends.sqlite.test_features_llm.BuildInstanceTests.test_uses_provided_db_name backends.sqlite.test_features_llm.DummyManager.__init__ backends.sqlite.test_features_llm.DummyManager.db_manager backends.sqlite.test_features_llm.DummyManager.get_by_natural_key backends.sqlite.test_features_llm.DummyModel.__init__ backends.sqlite.test_features_llm.DummyModel._make_meta backends.sqlite.test_features_llm.DummyPK.__init__ backends.sqlite.test_features_llm.[] (backends.sqlite.test_features_llm.DummyModel) backends.sqlite.test_features_llm.make_model_with_natural_key
coverage json -o coverage.json
: '>>>>> End Test Output'
