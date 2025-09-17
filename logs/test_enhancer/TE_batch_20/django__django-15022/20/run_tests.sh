#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 admin_changelist.test_admin_llm.SearchResultsRegressionTests._get_results admin_changelist.test_admin_llm.SearchResultsRegressionTests.setUp admin_changelist.test_admin_llm.SearchResultsRegressionTests.test_search_on_parent_model_using_child_lookup
coverage json -o coverage.json
: '>>>>> End Test Output'
