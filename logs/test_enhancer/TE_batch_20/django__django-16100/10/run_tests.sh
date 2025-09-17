#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 admin_changelist.tests_llm.test_atomic_used_when_log_change_raises admin_changelist.tests_llm.test_atomic_used_with_band_admin admin_changelist.tests_llm.test_atomic_used_with_child_admin_multiple_forms admin_changelist.tests_llm.test_atomic_used_with_child_admin_via_factory admin_changelist.tests_llm.test_atomic_used_with_concert_admin admin_changelist.tests_llm.test_atomic_used_with_group_admin admin_changelist.tests_llm.test_atomic_used_with_parent_admin admin_changelist.tests_llm.test_atomic_used_with_swallow_admin admin_changelist.tests_llm.test_atomic_used_with_swallow_admin_multiple_changes
coverage json -o coverage.json
: '>>>>> End Test Output'
