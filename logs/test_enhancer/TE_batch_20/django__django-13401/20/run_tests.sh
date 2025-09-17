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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 model_fields.tests_llm.FieldComparisonAndHashTests.test_bisect_insertion_respects_no_model_first model_fields.tests_llm.FieldComparisonAndHashTests.test_lt_consistency_when_creation_counter_equal model_fields.tests_llm.FieldComparisonAndHashTests.test_multiple_fields_mixed_ordering model_fields.tests_llm.FieldComparisonAndHashTests.test_no_model_field_is_less_than_model_field model_fields.tests_llm.FieldComparisonAndHashTests.test_sorted_stability_with_many_copies model_fields.tests_llm.FieldComparisonAndHashTests.test_sorting_respects_no_model_first model_fields.tests_llm.FieldHashTests.test_hash_bound_field_includes_model_meta model_fields.tests_llm.FieldHashTests.test_hash_unbound_field_includes_none_components
coverage json -o coverage.json
: '>>>>> End Test Output'
