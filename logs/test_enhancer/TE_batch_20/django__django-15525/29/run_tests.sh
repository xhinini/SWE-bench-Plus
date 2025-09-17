#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 backends.sqlite.test_features_llm.BuildInstanceTests.test_applies_pk_to_python backends.sqlite.test_features_llm.BuildInstanceTests.test_handles_does_not_exist backends.sqlite.test_features_llm.BuildInstanceTests.test_natural_key_sees_relation_field_from_data backends.sqlite.test_features_llm.BuildInstanceTests.test_no_get_by_natural_key_returns_model_without_pk_set backends.sqlite.test_features_llm.BuildInstanceTests.test_no_natural_key_method_returns_model backends.sqlite.test_features_llm.BuildInstanceTests.test_sets_state_db_before_natural_key_call backends.sqlite.test_features_llm.BuildInstanceTests.test_uses_db_in_get_by_natural_key_call backends.sqlite.test_features_llm.BuildInstanceTests.test_when_pk_present_skips_manager_call backends.sqlite.test_features_llm.BuildInstanceTests.test_with_pk_provided_returns_model_with_pk backends.sqlite.test_features_llm.DummyManager.__init__ backends.sqlite.test_features_llm.DummyManager.db_manager backends.sqlite.test_features_llm.DummyManager.get_by_natural_key backends.sqlite.test_features_llm.DummyPK.__init__ backends.sqlite.test_features_llm.DummyState.__init__ backends.sqlite.test_features_llm.make_model_class
coverage json -o coverage.json
: '>>>>> End Test Output'
