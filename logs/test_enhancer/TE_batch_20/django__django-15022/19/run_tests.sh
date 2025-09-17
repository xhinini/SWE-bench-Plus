#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 admin_changelist.test_admin_llm.GetSearchResultsTests.setUp admin_changelist.test_admin_llm.GetSearchResultsTests.test_case_insensitive_search admin_changelist.test_admin_llm.GetSearchResultsTests.test_m2m_search_spawns_duplicates_flag admin_changelist.test_admin_llm.GetSearchResultsTests.test_multi_term_search_all_terms_must_match admin_changelist.test_admin_llm.GetSearchResultsTests.test_prefix_lookup_search_behavior admin_changelist.test_admin_llm.GetSearchResultsTests.test_quoted_phrase_search_treated_as_single_term admin_changelist.test_admin_llm.GetSearchResultsTests.test_search_across_related_field admin_changelist.test_admin_llm.GetSearchResultsTests.test_search_ignores_nonexistent_related_field admin_changelist.test_admin_llm.GetSearchResultsTests.test_search_with_pk_lookup admin_changelist.test_admin_llm.GetSearchResultsTests.test_single_term_search_matches_child_name
coverage json -o coverage.json
: '>>>>> End Test Output'
