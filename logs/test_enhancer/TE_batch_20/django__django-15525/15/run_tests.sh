#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 backends.sqlite.test_features_llm.BuildInstanceTests.test_attribute_error_in_natural_key_propagates backends.sqlite.test_features_llm.BuildInstanceTests.test_natural_key_accessing_relational_attribute_uses_state_db backends.sqlite.test_features_llm.BuildInstanceTests.test_swallows_does_not_exist_exception backends.sqlite.test_features_llm.FakeManager.__init__ backends.sqlite.test_features_llm.FakeManager.db_manager backends.sqlite.test_features_llm.FakeManager.get_by_natural_key backends.sqlite.test_features_llm.PkField.__init__ backends.sqlite.test_features_llm.PkField.to_python backends.sqlite.test_features_llm.SimpleModelClassFactory.make_class
coverage json -o coverage.json
: '>>>>> End Test Output'
