#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 backends.sqlite.test_features_llm.BuildInstanceTests.test_multiple_different_dbs_are_used backends.sqlite.test_features_llm.BuildInstanceTests.test_natural_key_attribute_error_propagates backends.sqlite.test_features_llm.BuildInstanceTests.test_state_db_used_in_natural_key_and_lookup backends.sqlite.test_features_llm.RecordingManager.__init__ backends.sqlite.test_features_llm.RecordingManager.db_manager backends.sqlite.test_features_llm.RecordingManager.get_by_natural_key backends.sqlite.test_features_llm.make_model
coverage json -o coverage.json
: '>>>>> End Test Output'
