#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 admin_changelist.test_admin_llm.GetSearchResultsTests._admin_for_parent admin_changelist.test_admin_llm.GetSearchResultsTests.setUp admin_changelist.test_admin_llm.GetSearchResultsTests.test_multi_term_no_match admin_changelist.test_admin_llm.GetSearchResultsTests.test_multi_term_search_and_behavior admin_changelist.test_admin_llm.GetSearchResultsTests.test_multiple_search_fields_and_terms admin_changelist.test_admin_llm.GetSearchResultsTests.test_prefix_exact_operator admin_changelist.test_admin_llm.GetSearchResultsTests.test_prefix_search_operator_at admin_changelist.test_admin_llm.GetSearchResultsTests.test_prefix_startswith_operator admin_changelist.test_admin_llm.GetSearchResultsTests.test_quoted_term_with_space admin_changelist.test_admin_llm.GetSearchResultsTests.test_search_pk_token_replacement admin_changelist.test_admin_llm.GetSearchResultsTests.test_single_term_related_field
coverage json -o coverage.json
: '>>>>> End Test Output'
