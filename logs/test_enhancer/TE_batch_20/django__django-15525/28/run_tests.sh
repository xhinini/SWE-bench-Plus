#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 backends.sqlite.test_features_llm.BuildInstanceTests.test_db_passed_to_db_manager backends.sqlite.test_features_llm.BuildInstanceTests.test_existing_pk_preserved backends.sqlite.test_features_llm.BuildInstanceTests.test_handles_manager_raises_doesnotexist backends.sqlite.test_features_llm.BuildInstanceTests.test_missing_fk_attname_causes_no_pk_if_not_set backends.sqlite.test_features_llm.BuildInstanceTests.test_natural_key_with_multiple_elements_including_fk backends.sqlite.test_features_llm.BuildInstanceTests.test_no_get_by_natural_key_on_manager backends.sqlite.test_features_llm.BuildInstanceTests.test_non_string_pk_conversion backends.sqlite.test_features_llm.BuildInstanceTests.test_pk_set_when_fk_field_is_non_remote backends.sqlite.test_features_llm.BuildInstanceTests.test_pk_set_when_fk_field_is_remote_and_data_contains_attname backends.sqlite.test_features_llm.BuildInstanceTests.test_to_python_called_on_pk backends.sqlite.test_features_llm.DummyManager.__init__ backends.sqlite.test_features_llm.DummyManager.db_manager backends.sqlite.test_features_llm.DummyManager.get_by_natural_key backends.sqlite.test_features_llm.DummyPK.__init__ backends.sqlite.test_features_llm.DummyPK.to_python backends.sqlite.test_features_llm.make_model
coverage json -o coverage.json
: '>>>>> End Test Output'
