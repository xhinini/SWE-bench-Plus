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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 model_fields.tests_llm.FieldOrderingRegressionTests._make_model model_fields.tests_llm.FieldOrderingRegressionTests.test_le_and_ge_consistency_for_model_and_no_model model_fields.tests_llm.FieldOrderingRegressionTests.test_no_model_field_less_than_model_field_with_equal_creation_counter model_fields.tests_llm.FieldOrderingRegressionTests.test_sorted_puts_no_model_fields_first_when_creation_counter_equal model_fields.tests_llm.FieldOrderingRegressionTests.test_sorting_preserves_consistency_when_some_fields_unattached
coverage json -o coverage.json
: '>>>>> End Test Output'
