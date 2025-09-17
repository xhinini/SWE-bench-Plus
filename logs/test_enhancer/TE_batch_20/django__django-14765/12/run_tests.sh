#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 migrations.test_state_llm.ProjectStateRealAppsTests.test_accepts_empty_set migrations.test_state_llm.ProjectStateRealAppsTests.test_accepts_set migrations.test_state_llm.ProjectStateRealAppsTests.test_none_uses_empty_set migrations.test_state_llm.ProjectStateRealAppsTests.test_rejects_bytes migrations.test_state_llm.ProjectStateRealAppsTests.test_rejects_empty_list migrations.test_state_llm.ProjectStateRealAppsTests.test_rejects_frozenset migrations.test_state_llm.ProjectStateRealAppsTests.test_rejects_generator migrations.test_state_llm.ProjectStateRealAppsTests.test_rejects_list migrations.test_state_llm.ProjectStateRealAppsTests.test_rejects_string migrations.test_state_llm.ProjectStateRealAppsTests.test_rejects_tuple
coverage json -o coverage.json
: '>>>>> End Test Output'
