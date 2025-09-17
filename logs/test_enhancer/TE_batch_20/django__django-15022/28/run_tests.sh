#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 admin_changelist.test_admin_llm.GetSearchResultsTests._get_qs_pks admin_changelist.test_admin_llm.GetSearchResultsTests.setUp admin_changelist.test_admin_llm.GetSearchResultsTests.test_exact_lookup_equals_prefix admin_changelist.test_admin_llm.GetSearchResultsTests.test_multiple_terms_all_must_match admin_changelist.test_admin_llm.GetSearchResultsTests.test_prefix_lookup_startswith admin_changelist.test_admin_llm.GetSearchResultsTests.test_quoted_phrase_treated_as_single_term admin_changelist.test_admin_llm.GetSearchResultsTests.test_search_respects_dynamic_search_fields admin_changelist.test_admin_llm.GetSearchResultsTests.test_search_returns_empty_when_no_match admin_changelist.test_admin_llm.GetSearchResultsTests.test_single_term_single_field admin_changelist.test_admin_llm.GetSearchResultsTests.test_swallow_list_editable_search_ok admin_changelist.test_admin_llm.GetSearchResultsTests.test_two_terms_and_across_fields
coverage json -o coverage.json
: '>>>>> End Test Output'
