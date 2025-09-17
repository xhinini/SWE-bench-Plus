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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 ordering.test_models_llm.DummyField.__init__ ordering.test_models_llm.DummyQuery.__init__ ordering.test_models_llm.DummyQuery.trim_joins ordering.test_models_llm.FindOrderingNameTests.assert_orderbys_from_transform ordering.test_models_llm.FindOrderingNameTests.make_compiler_with_setup ordering.test_models_llm.FindOrderingNameTests.test_alias_passed_to_transform ordering.test_models_llm.FindOrderingNameTests.test_attname_matches_even_with_unrelated_opts_passed ordering.test_models_llm.FindOrderingNameTests.test_descending_with_multiple_targets ordering.test_models_llm.FindOrderingNameTests.test_different_target_objects ordering.test_models_llm.FindOrderingNameTests.test_last_piece_match_with_complex_target_names ordering.test_models_llm.FindOrderingNameTests.test_nested_last_piece_match_three_levels ordering.test_models_llm.FindOrderingNameTests.test_simple_last_piece_match ordering.test_models_llm.FindOrderingNameTests.test_simple_last_piece_match_with_minus_prefix ordering.test_models_llm.FindOrderingNameTests.test_single_piece_last_equals_attname
coverage json -o coverage.json
: '>>>>> End Test Output'
