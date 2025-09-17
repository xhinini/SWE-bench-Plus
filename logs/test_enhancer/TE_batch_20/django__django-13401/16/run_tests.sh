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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 model_fields.tests_llm.FieldComparisonPatchTests.make_field model_fields.tests_llm.FieldComparisonPatchTests.test_bisect_insort_respects_field_ordering model_fields.tests_llm.FieldComparisonPatchTests.test_model_order_after_no_model_when_equal_creation_counter model_fields.tests_llm.FieldComparisonPatchTests.test_no_model_order_before_model_when_equal_creation_counter model_fields.tests_llm.FieldComparisonPatchTests.test_sorted_places_no_model_first_when_equal_counters
coverage json -o coverage.json
: '>>>>> End Test Output'
