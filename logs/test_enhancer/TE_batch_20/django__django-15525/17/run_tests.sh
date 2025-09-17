#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 backends.sqlite.test_features_llm.BuildInstanceTests.test_natural_key_requires_state_db_and_build_sets_it backends.sqlite.test_features_llm.BuildInstanceTests.test_preserves_other_fields_from_data backends.sqlite.test_features_llm.DefaultManager.__init__ backends.sqlite.test_features_llm.DefaultManager.db_manager backends.sqlite.test_features_llm.DefaultManager.get_by_natural_key backends.sqlite.test_features_llm.FakeMeta.__init__ backends.sqlite.test_features_llm.FakeModel.__init__ backends.sqlite.test_features_llm.FakeModel.__repr__ backends.sqlite.test_features_llm.FakeState.__init__ backends.sqlite.test_features_llm.PKField.__init__ backends.sqlite.test_features_llm.PKField.to_python
coverage json -o coverage.json
: '>>>>> End Test Output'
