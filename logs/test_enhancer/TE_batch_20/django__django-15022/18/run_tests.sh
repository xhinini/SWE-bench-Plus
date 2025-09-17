#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 admin_changelist.test_admin_llm.SearchTests._get_results admin_changelist.test_admin_llm.SearchTests.setUp admin_changelist.test_admin_llm.SearchTests.test_nonexistent_field_in_search_is_ignored
coverage json -o coverage.json
: '>>>>> End Test Output'
