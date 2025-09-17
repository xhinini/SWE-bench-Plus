#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 admin_changelist.test_admin_llm.GetSearchResultsTests._request admin_changelist.test_admin_llm.GetSearchResultsTests.setUp admin_changelist.test_admin_llm.GetSearchResultsTests.test_may_have_duplicates_flag_for_relational_lookups admin_changelist.test_admin_llm.GetSearchResultsTests.test_multiple_fields_single_term admin_changelist.test_admin_llm.GetSearchResultsTests.test_multiple_terms_and_logic admin_changelist.test_admin_llm.GetSearchResultsTests.test_multiple_tokens_do_not_match_if_one_missing admin_changelist.test_admin_llm.GetSearchResultsTests.test_nonexistent_field_is_ignored admin_changelist.test_admin_llm.GetSearchResultsTests.test_prefix_lookup_startswith_and_exact admin_changelist.test_admin_llm.GetSearchResultsTests.test_quoted_term_with_space admin_changelist.test_admin_llm.GetSearchResultsTests.test_related_field_lookup admin_changelist.test_admin_llm.GetSearchResultsTests.test_single_term_single_field
coverage json -o coverage.json
: '>>>>> End Test Output'
