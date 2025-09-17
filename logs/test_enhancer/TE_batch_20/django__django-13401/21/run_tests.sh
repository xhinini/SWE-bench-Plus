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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 model_fields.tests_llm.DummyMeta.__init__ model_fields.tests_llm.DummyModel.__init__ model_fields.tests_llm.FieldComparisonHashingTests.make_field model_fields.tests_llm.FieldComparisonHashingTests.test_field_sorting_stable model_fields.tests_llm.FieldComparisonHashingTests.test_lt_both_models_case_sensitive_label_vs_model_name model_fields.tests_llm.FieldComparisonHashingTests.test_lt_fields_both_no_model_equal_creation_counter model_fields.tests_llm.FieldComparisonHashingTests.test_lt_model_vs_no_model
coverage json -o coverage.json
: '>>>>> End Test Output'
