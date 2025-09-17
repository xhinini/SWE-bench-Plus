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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 model_fields.tests_llm.FieldComparisonTests.test_bisect_insertion_maintains_expected_order model_fields.tests_llm.FieldComparisonTests.test_hash_includes_model_meta_for_model_field model_fields.tests_llm.FieldComparisonTests.test_hash_includes_none_for_no_model_field model_fields.tests_llm.FieldComparisonTests.test_model_field_ordering_uses_model_name_lowercase model_fields.tests_llm.FieldComparisonTests.test_no_model_less_than_model_when_counters_equal model_fields.tests_llm.FieldComparisonTests.test_sorted_fields_order_with_mixed_model_presence
coverage json -o coverage.json
: '>>>>> End Test Output'
