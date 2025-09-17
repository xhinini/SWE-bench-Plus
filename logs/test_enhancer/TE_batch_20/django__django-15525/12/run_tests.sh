#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 backends.sqlite.test_features_llm.BuildInstanceTests.test_build_instance_works_with_non_string_db_identifiers backends.sqlite.test_features_llm.BuildInstanceTests.test_multiple_dbs_produce_different_pks backends.sqlite.test_features_llm.BuildInstanceTests.test_natural_key_may_depend_on_other_fields_but_db_used backends.sqlite.test_features_llm.BuildInstanceTests.test_sets_pk_using_natural_key_and_db backends.sqlite.test_features_llm.BuildInstanceTests.test_to_python_conversion_is_applied backends.sqlite.test_features_llm.DummyManager.__init__ backends.sqlite.test_features_llm.DummyManager.db_manager backends.sqlite.test_features_llm.DummyManager.get_by_natural_key backends.sqlite.test_features_llm.DummyPK.__init__ backends.sqlite.test_features_llm.DummyPK.to_python backends.sqlite.test_features_llm.make_model
coverage json -o coverage.json
: '>>>>> End Test Output'
