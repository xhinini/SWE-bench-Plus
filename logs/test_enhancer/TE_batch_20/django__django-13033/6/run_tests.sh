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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 ordering.test_models_llm.DummyExpr.__init__ ordering.test_models_llm.DummyExpr.__repr__ ordering.test_models_llm.DummyField.__init__ ordering.test_models_llm.DummyQuery.__init__ ordering.test_models_llm.DummyQuery.trim_joins ordering.test_models_llm.FindOrderingNameTests.test_attname_matches_last_piece_no_default_ordering ordering.test_models_llm.FindOrderingNameTests.test_attname_matches_last_piece_no_default_ordering_descending ordering.test_models_llm.FindOrderingNameTests.test_find_ordering_name_with_numeric_like_suffix ordering.test_models_llm.FindOrderingNameTests.test_find_ordering_name_with_unusual_alias ordering.test_models_llm.FindOrderingNameTests.test_hyphen_in_name_produces_descending_ordering ordering.test_models_llm.FindOrderingNameTests.test_last_piece_comparison_uses_last_segment_not_full_lookup ordering.test_models_llm.FindOrderingNameTests.test_multiple_targets_with_attname_match ordering.test_models_llm.FindOrderingNameTests.test_name_is_pk_avoids_appending_default_ordering ordering.test_models_llm.FindOrderingNameTests.test_non_relation_field_returns_transforms ordering.test_models_llm.FindOrderingNameTests.test_single_target_with_attname_match ordering.test_models_llm.make_compiler
coverage json -o coverage.json
: '>>>>> End Test Output'
