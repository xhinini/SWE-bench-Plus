#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 backends.sqlite.test_features_llm.BuildInstanceTests.test_does_not_modify_unrelated_data_keys backends.sqlite.test_features_llm.BuildInstanceTests.test_natural_key_returning_iterable_tuple backends.sqlite.test_features_llm.BuildInstanceTests.test_sets_pk_using_natural_key_and_db_on_instance backends.sqlite.test_features_llm.BuildInstanceTests.test_with_foreignkey_attname_in_data_does_not_call_meta_get_field backends.sqlite.test_features_llm.DummyManager.__init__ backends.sqlite.test_features_llm.DummyManager.db_manager backends.sqlite.test_features_llm.DummyManager.get_by_natural_key backends.sqlite.test_features_llm.DummyMeta.__init__ backends.sqlite.test_features_llm.DummyMeta.get_field backends.sqlite.test_features_llm.DummyModelBase.__init__ backends.sqlite.test_features_llm.DummyModelBase.__repr__ backends.sqlite.test_features_llm.DummyModelFactory.create backends.sqlite.test_features_llm.DummyPK.__init__ backends.sqlite.test_features_llm.DummyState.__init__ backends.sqlite.test_features_llm.[] (backends.sqlite.test_features_llm.DummyModelBase)
coverage json -o coverage.json
: '>>>>> End Test Output'
