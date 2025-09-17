#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 backends.sqlite.test_features_llm.BuildInstanceTests.test_compound_natural_key_with_mixed_fields backends.sqlite.test_features_llm.BuildInstanceTests.test_natural_key_attribute_error_propagates backends.sqlite.test_features_llm.BuildInstanceTests.test_natural_key_depends_on_relation_field_present_in_data backends.sqlite.test_features_llm.DummyManager.__init__ backends.sqlite.test_features_llm.DummyManager.db_manager backends.sqlite.test_features_llm.DummyManager.get_by_natural_key backends.sqlite.test_features_llm.DummyPK.__init__ backends.sqlite.test_features_llm.DummyPK.to_python backends.sqlite.test_features_llm.make_model_class
coverage json -o coverage.json
: '>>>>> End Test Output'
