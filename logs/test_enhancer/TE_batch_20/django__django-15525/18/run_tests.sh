#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 backends.sqlite.test_features_llm.BuildInstanceTests.test_handles_does_not_exist_from_manager backends.sqlite.test_features_llm.BuildInstanceTests.test_multiple_build_instance_calls_use_provided_db_each_time backends.sqlite.test_features_llm.BuildInstanceTests.test_natural_key_accesses_related_and_sees_state_db backends.sqlite.test_features_llm.BuildInstanceTests.test_sets_state_db_before_natural_key
coverage json -o coverage.json
: '>>>>> End Test Output'
