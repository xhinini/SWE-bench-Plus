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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 model_fields.tests_llm.FieldOrderingHashTests.test_bisect_insort_respects_field_ordering model_fields.tests_llm.FieldOrderingHashTests.test_gt_with_model_and_no_model model_fields.tests_llm.FieldOrderingHashTests.test_hash_diff_for_models_with_same_counter model_fields.tests_llm.FieldOrderingHashTests.test_hash_no_model_matches_expected_tuple model_fields.tests_llm.FieldOrderingHashTests.test_lt_no_model_vs_model_counters_equal model_fields.tests_llm.FieldOrderingHashTests.test_lt_with_other_type_returns_notimplemented model_fields.tests_llm.FieldOrderingHashTests.test_set_uniqueness_with_model_and_counter model_fields.tests_llm.FieldOrderingHashTests.test_sort_mixed_field_list_places_no_model_first model_fields.tests_llm.FieldOrderingHashTests.test_sort_stability_multiple_fields
coverage json -o coverage.json
: '>>>>> End Test Output'
