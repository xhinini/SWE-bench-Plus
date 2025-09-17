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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 model_fields.tests_llm.FieldOrderingRegressionTests.test_model_field_greater_than_no_model_field_when_reversed model_fields.tests_llm.FieldOrderingRegressionTests.test_no_model_field_less_than_model_field model_fields.tests_llm.FieldOrderingRegressionTests.test_sort_mixed_fields_places_no_model_first
coverage json -o coverage.json
: '>>>>> End Test Output'
