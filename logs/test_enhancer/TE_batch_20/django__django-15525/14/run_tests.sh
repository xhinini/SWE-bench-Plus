#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 backends.sqlite.test_features_llm.BuildInstanceTests.test_attribute_error_from_natural_key_propagates backends.sqlite.test_features_llm.BuildInstanceTests.test_converts_pk_using_to_python backends.sqlite.test_features_llm.BuildInstanceTests.test_handles_empty_natural_key_components backends.sqlite.test_features_llm.BuildInstanceTests.test_handles_natural_key_returning_string_by_splatting_chars backends.sqlite.test_features_llm.BuildInstanceTests.test_multiple_calls_preserve_and_update_data_correctly backends.sqlite.test_features_llm.BuildInstanceTests.test_passes_multiple_natural_key_components_to_manager backends.sqlite.test_features_llm.BuildInstanceTests.test_sets_pk_and_mutates_data_when_natural_key_found_and_state_db_set backends.sqlite.test_features_llm.DummyDBManager.__init__ backends.sqlite.test_features_llm.DummyDBManager.get_by_natural_key backends.sqlite.test_features_llm.DummyDefaultManager.__init__ backends.sqlite.test_features_llm.DummyDefaultManager.db_manager backends.sqlite.test_features_llm.DummyManagerResult.__init__ backends.sqlite.test_features_llm.DummyPK.__init__ backends.sqlite.test_features_llm.DummyPK.to_python backends.sqlite.test_features_llm.make_model_class
coverage json -o coverage.json
: '>>>>> End Test Output'
