#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 admin_changelist.test_admin_llm.GetSearchResultsTests._admin_for admin_changelist.test_admin_llm.GetSearchResultsTests.setUp admin_changelist.test_admin_llm.GetSearchResultsTests.test_multiple_terms_with_relation_lookup admin_changelist.test_admin_llm.GetSearchResultsTests.test_quoted_phrase_treated_as_single_term
coverage json -o coverage.json
: '>>>>> End Test Output'
