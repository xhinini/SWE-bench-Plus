#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 admin_changelist.test_admin_llm.GetSearchResultsTests.setUp admin_changelist.test_admin_llm.GetSearchResultsTests.test_many_to_many_may_have_duplicates_flag admin_changelist.test_admin_llm.GetSearchResultsTests.test_multi_term_and_across_fields admin_changelist.test_admin_llm.GetSearchResultsTests.test_multi_term_related_and admin_changelist.test_admin_llm.GetSearchResultsTests.test_multiple_bits_and_or_behavior_with_m2m_and_fk admin_changelist.test_admin_llm.GetSearchResultsTests.test_quoted_phrase_treated_as_single_term admin_changelist.test_admin_llm.GetSearchResultsTests.test_search_prefix_and_exact_lookups admin_changelist.test_admin_llm.GetSearchResultsTests.test_search_related_fk admin_changelist.test_admin_llm.GetSearchResultsTests.test_search_with_pk_alias admin_changelist.test_admin_llm.GetSearchResultsTests.test_single_term_local_field
coverage json -o coverage.json
: '>>>>> End Test Output'
