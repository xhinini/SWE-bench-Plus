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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 model_fields.tests_llm.DummyMeta.__init__ model_fields.tests_llm.DummyModel.__init__ model_fields.tests_llm.FieldComparisonHashingTests.test_eq_considers_model_diff_models_not_equal model_fields.tests_llm.FieldComparisonHashingTests.test_eq_same_model_and_counter_equal model_fields.tests_llm.FieldComparisonHashingTests.test_hash_consistent_with_eq model_fields.tests_llm.FieldComparisonHashingTests.test_hash_none_model_included model_fields.tests_llm.FieldComparisonHashingTests.test_hash_uses_model_meta_app_label_and_model_name model_fields.tests_llm.FieldComparisonHashingTests.test_lt_model_vs_model_with_equal_counter_orders_by_meta_tuple model_fields.tests_llm.FieldComparisonHashingTests.test_lt_no_model_before_model_when_counters_equal model_fields.tests_llm.FieldComparisonHashingTests.test_no_model_fields_equal_counters_not_less_than_each_other model_fields.tests_llm.FieldComparisonHashingTests.test_sort_mixed_fields_orders_no_model_first model_fields.tests_llm.FieldComparisonHashingTests.test_sort_stable_for_many_fields
coverage json -o coverage.json
: '>>>>> End Test Output'
