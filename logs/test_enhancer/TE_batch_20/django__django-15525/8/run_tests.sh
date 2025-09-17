#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 backends.sqlite.test_features_llm.BuildInstanceTests.test_db_none_is_supported backends.sqlite.test_features_llm.BuildInstanceTests.test_handles_does_not_exist_from_get_by_natural_key backends.sqlite.test_features_llm.BuildInstanceTests.test_missing_natural_key_attribute_skips_behavior backends.sqlite.test_features_llm.BuildInstanceTests.test_multiple_calls_with_different_db_values backends.sqlite.test_features_llm.BuildInstanceTests.test_natural_key_based_on_other_field backends.sqlite.test_features_llm.BuildInstanceTests.test_natural_key_call_avoids_attribute_error_with_db_set backends.sqlite.test_features_llm.BuildInstanceTests.test_no_get_by_natural_key_attribute backends.sqlite.test_features_llm.BuildInstanceTests.test_returns_model_instance_with_preserved_fields backends.sqlite.test_features_llm.BuildInstanceTests.test_sets_db_on_obj_before_natural_key backends.sqlite.test_features_llm.BuildInstanceTests.test_skips_natural_key_when_pk_present backends.sqlite.test_features_llm.FakeManager.__init__ backends.sqlite.test_features_llm.FakeManager.db_manager backends.sqlite.test_features_llm.FakeMeta.__init__ backends.sqlite.test_features_llm.FakeModelBase.__init__ backends.sqlite.test_features_llm.FakeModelBase.__repr__ backends.sqlite.test_features_llm.FakePK.__init__ backends.sqlite.test_features_llm.FakePK.to_python
coverage json -o coverage.json
: '>>>>> End Test Output'
