#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 admin_changelist.test_admin_llm.ConstructSearchTests._get_search_results admin_changelist.test_admin_llm.ConstructSearchTests.setUp admin_changelist.test_admin_llm.ConstructSearchTests.test_mixed_case_matching admin_changelist.test_admin_llm.ConstructSearchTests.test_multi_term_across_fields admin_changelist.test_admin_llm.ConstructSearchTests.test_non_matching_returns_empty admin_changelist.test_admin_llm.ConstructSearchTests.test_order_independent_terms admin_changelist.test_admin_llm.ConstructSearchTests.test_phrase_with_extra_spaces admin_changelist.test_admin_llm.ConstructSearchTests.test_prefix_and_exact_prefix_lookup admin_changelist.test_admin_llm.ConstructSearchTests.test_quoted_phrase_matching admin_changelist.test_admin_llm.ConstructSearchTests.test_single_term_exact_word admin_changelist.test_admin_llm.ConstructSearchTests.test_two_terms_and_logic
coverage json -o coverage.json
: '>>>>> End Test Output'
