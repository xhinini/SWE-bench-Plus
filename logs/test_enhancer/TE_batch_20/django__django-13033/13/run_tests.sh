#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
sed -i '/en_US.UTF-8/s/^# //g' /etc/locale.gen && locale-gen
export LANG=en_US.UTF-8
export LANGUAGE=en_US:en
export LC_ALL=en_US.UTF-8
export PYTHONIOENCODING=utf8
python --version && python -m pip install -U pip
python -m pip install -U 'coverage==6.2'

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 ordering.test_models_llm.FindOrderingNameTests.test_alias_argument_ignored_for_matching_attname ordering.test_models_llm.FindOrderingNameTests.test_default_order_asc_passed_to_orderby_on_match ordering.test_models_llm.FindOrderingNameTests.test_default_order_desc_passed_to_orderby_on_match ordering.test_models_llm.FindOrderingNameTests.test_descending_skip_relation_when_last_piece_matches_attname ordering.test_models_llm.FindOrderingNameTests.test_multiple_level_field_last_piece_matches_attname ordering.test_models_llm.FindOrderingNameTests.test_negative_multiple_level_field_last_piece_matches_attname ordering.test_models_llm.FindOrderingNameTests.test_no_false_positive_when_attname_matches_but_full_name_differs ordering.test_models_llm.FindOrderingNameTests.test_single_target_returns_single_orderby ordering.test_models_llm.FindOrderingNameTests.test_skip_relation_when_last_piece_matches_attname ordering.test_models_llm.FindOrderingNameTests.test_with_empty_opts_ordering_still_returns_targets ordering.test_models_llm._make_compiler ordering.test_models_llm.compile_orderings
coverage json -o coverage.json
: '>>>>> End Test Output'
