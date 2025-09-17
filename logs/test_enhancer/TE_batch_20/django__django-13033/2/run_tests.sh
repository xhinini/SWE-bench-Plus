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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 ordering.test_models_llm.FindOrderingNameTests._make_compiler_with_stub ordering.test_models_llm.FindOrderingNameTests._make_opts_with_ordering ordering.test_models_llm.FindOrderingNameTests.test_includes_related_model_ordering_for_complex_lookup_ending_with_id ordering.test_models_llm.FindOrderingNameTests.test_includes_related_model_ordering_for_record_root_id ordering.test_models_llm.FindOrderingNameTests.test_includes_related_ordering_when_attname_differs_from_last_piece_and_endswith_id ordering.test_models_llm.FindOrderingNameTests.test_multiple_related_ordering_entries_appended_for_id_suffix ordering.test_models_llm.FindOrderingNameTests.test_no_false_positive_when_field_attname_matches_last_piece_even_if_endswith_id ordering.test_models_llm.FindOrderingNameTests.test_preserves_related_ordering_when_name_has_leading_minus_and_endswith_id ordering.test_models_llm.FindOrderingNameTests.test_related_ordering_appended_for_deep_lookup_ending_with_id ordering.test_models_llm.FindOrderingNameTests.test_related_ordering_appended_for_many_targets_when_lookup_endswith_id ordering.test_models_llm.FindOrderingNameTests.test_related_ordering_appended_when_ordering_is_orderby_instance ordering.test_models_llm.FindOrderingNameTests.test_related_ordering_appended_with_mixed_case_name_ending_with_id
coverage json -o coverage.json
: '>>>>> End Test Output'
